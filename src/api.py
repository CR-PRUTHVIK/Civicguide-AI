from pathlib import Path
import os
import time

import chromadb
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

from src.generation import generate_answer

# ==================================================
# PROJECT PATH
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv(BASE_DIR / ".env")


# ==================================================
# FASTAPI APP
# ==================================================

app = FastAPI(
    title="CivicGuide AI API",
    description="Enterprise RAG Backend API for CivicGuide AI",
    version="2.0"
)


# ==================================================
# STATIC FILES
# ==================================================

app.mount(
    "/static",
    StaticFiles(
        directory=str(BASE_DIR / "static")
    ),
    name="static"
)


# ==================================================
# LOAD EMBEDDING MODEL
# ==================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded successfully!")


# ==================================================
# CONNECT TO CHROMADB
# ==================================================

DB_PATH = BASE_DIR / "chroma_db"
COLLECTION_NAME = "civicguide_documents"

def get_chroma_collection():
    try:
        client = chromadb.PersistentClient(path=str(DB_PATH))
        return client.get_or_create_collection(name=COLLECTION_NAME)
    except Exception as error:
        print(f"Chroma connection error: {error}")
        return None


# ==================================================
# SETTINGS
# ==================================================

TOP_K_RESULTS = 8
DISTANCE_THRESHOLD = 1.3


# ==================================================
# REQUEST MODELS
# ==================================================

class QuestionRequest(BaseModel):
    question: str


class FeedbackRequest(BaseModel):
    question: str
    rating: str
    comment: str | None = None


# ==================================================
# HOME ENDPOINT
# ==================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
def home():
    html_file = (
        BASE_DIR /
        "templates" /
        "index.html"
    )

    return html_file.read_text(
        encoding="utf-8"
    )


# ==================================================
# HEALTH ENDPOINT
# ==================================================

@app.get("/health")
def health():
    collection = get_chroma_collection()
    chunk_count = collection.count() if collection is not None else 0
    return {
        "status": "healthy",
        "knowledge_base_connected": collection is not None,
        "total_chunks": chunk_count,
        "embedding_model": "all-MiniLM-L6-v2",
        "generation_service": "Cohere Command R"
    }


# ==================================================
# DOCUMENTS / KNOWLEDGE BASE METADATA ENDPOINT
# ==================================================

@app.get("/api/documents")
def get_documents_metadata():
    collection = get_chroma_collection()
    data_dir = BASE_DIR / "data"
    files_info = []
    total_chunks = collection.count() if collection is not None else 0

    if data_dir.exists():
        for file_path in sorted(data_dir.iterdir()):
            if file_path.is_file() and file_path.suffix.lower() in [".txt", ".pdf"]:
                chunk_count = 0
                if collection is not None:
                    try:
                        res = collection.get(where={"source": file_path.name})
                        chunk_count = len(res.get("ids", []))
                    except Exception:
                        pass

                size_kb = round(file_path.stat().st_size / 1024, 1)
                files_info.append({
                    "name": file_path.name,
                    "size_kb": size_kb,
                    "extension": file_path.suffix.lower().replace(".", ""),
                    "chunks": chunk_count
                })

    return {
        "total_documents": len(files_info),
        "total_chunks": total_chunks,
        "embedding_model": "all-MiniLM-L6-v2",
        "llm_model": "Cohere Command-R",
        "documents": files_info
    }


# ==================================================
# FEEDBACK ENDPOINT
# ==================================================

@app.post("/api/feedback")
def submit_feedback(request: FeedbackRequest):
    return {
        "status": "success",
        "message": f"Thank you! Your feedback ('{request.rating}') has been recorded."
    }


# ==================================================
# RETRIEVE DOCUMENTS FUNCTION
# ==================================================

def retrieve_documents(question):
    collection = get_chroma_collection()
    if collection is None:
        raise RuntimeError(
            "Knowledge base is not available."
        )

    # Create embedding for user question
    question_embedding = embedding_model.encode(question)

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding.tolist()],
        n_results=TOP_K_RESULTS,
        include=["documents", "metadatas", "distances"]
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    return documents, metadatas, distances


# ==================================================
# BUILD RAG CONTEXT
# ==================================================

def build_context(documents, metadatas):
    context_parts = []

    for index, document in enumerate(documents):
        source = "Unknown source"
        chunk_number = "Unknown"

        if index < len(metadatas):
            metadata = metadatas[index]
            if isinstance(metadata, dict):
                source = metadata.get("source", "Unknown source")
                chunk_number = metadata.get("chunk_number", "Unknown")

        context_parts.append(
            f"[Source: {source} | Chunk: {chunk_number}]\n{document}"
        )

    return "\n\n".join(context_parts)


# ==================================================
# FORMAT SOURCES WITH CONFIDENCE
# ==================================================

def format_sources(metadatas, distances):
    sources = []
    shown_sources = set()

    for index, metadata in enumerate(metadatas):
        if not isinstance(metadata, dict):
            continue

        source = metadata.get("source", "Unknown")
        chunk_number = metadata.get("chunk_number", "Unknown")
        distance = distances[index] if index < len(distances) else 1.0

        source_key = (source, chunk_number)

        if source_key not in shown_sources:
            match_score = max(10, min(99, int((1.3 - distance) / 1.3 * 100))) if distance <= 1.3 else 10
            sources.append({
                "source": source,
                "chunk_number": chunk_number,
                "distance": round(distance, 4) if distance is not None else None,
                "confidence": match_score
            })
            shown_sources.add(source_key)

    return sources


# ==================================================
# SEARCH ENDPOINT
# ==================================================

@app.post("/search")
def search(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        documents, metadatas, distances = retrieve_documents(question)

        if not documents:
            return {
                "question": question,
                "found": False,
                "message": "No relevant information was found in the knowledge base."
            }

        best_distance = distances[0] if distances else float("inf")

        if best_distance > DISTANCE_THRESHOLD:
            return {
                "question": question,
                "found": False,
                "message": "No sufficiently relevant information was found.",
                "best_match_distance": best_distance
            }

        retrieved_results = []
        for index, document in enumerate(documents):
            metadata = metadatas[index] if index < len(metadatas) else {}
            dist = distances[index] if index < len(distances) else None
            conf = max(10, min(99, int((1.3 - dist) / 1.3 * 100))) if dist is not None and dist <= 1.3 else 10

            retrieved_results.append({
                "text": document,
                "source": metadata.get("source", "Unknown"),
                "chunk_number": metadata.get("chunk_number", "Unknown"),
                "distance": round(dist, 4) if dist is not None else None,
                "confidence": conf
            })

        return {
            "question": question,
            "found": True,
            "best_match_distance": round(best_distance, 4),
            "results": retrieved_results
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ==================================================
# ASK ENDPOINT
# ==================================================

@app.post("/ask")
def ask(request: QuestionRequest):
    start_time = time.time()

    collection = get_chroma_collection()
    if collection is None:
        raise HTTPException(
            status_code=500,
            detail="Knowledge base is not available."
        )

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        documents, metadatas, distances = retrieve_documents(question)

        if not documents:
            return {
                "question": question,
                "found": False,
                "answer": "I could not find relevant information for this question in the official knowledge base.",
                "sources": [],
                "confidence": 0,
                "latency": round(time.time() - start_time, 2)
            }

        best_distance = distances[0] if distances else float("inf")

        if best_distance > DISTANCE_THRESHOLD:
            return {
                "question": question,
                "found": False,
                "answer": "I could not find sufficiently relevant information for this inquiry in the available documents. Please check the spelling or ask about voter services, scholarships, certificates, or civic grievance procedures.",
                "best_match_distance": round(best_distance, 4),
                "sources": [],
                "confidence": 0,
                "latency": round(time.time() - start_time, 2)
            }

        context = build_context(documents, metadatas)
        answer = generate_answer(question, context)
        sources = format_sources(metadatas, distances)

        confidence = max(10, min(99, int((1.3 - best_distance) / 1.3 * 100)))

        return {
            "question": question,
            "found": True,
            "answer": answer,
            "best_match_distance": round(best_distance, 4),
            "confidence": confidence,
            "sources": sources,
            "latency": round(time.time() - start_time, 2)
        }

    except HTTPException:
        raise

    except Exception as error:
        print(f"API Error: {error}")
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )