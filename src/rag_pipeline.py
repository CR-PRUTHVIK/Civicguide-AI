from pathlib import Path
import os

import chromadb
import cohere
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# ==================================================
# PROJECT PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "chroma_db"

# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv(BASE_DIR / ".env")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise ValueError(
        "COHERE_API_KEY was not found.\nPlease check your .env file."
    )

# ==================================================
# SETTINGS
# ==================================================

COLLECTION_NAME = "civicguide_documents"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COHERE_MODEL = "command-r-08-2024"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 8
DISTANCE_THRESHOLD = 1.3

# ==================================================
# LOAD EMBEDDING MODEL
# ==================================================

print("Loading embedding model...")
embedding_model = SentenceTransformer(EMBEDDING_MODEL)
print("Embedding model loaded successfully!")

# ==================================================
# CONNECT TO CHROMADB
# ==================================================

chroma_client = chromadb.PersistentClient(path=str(DB_PATH))


def read_txt_file(file_path):
    return file_path.read_text(encoding="utf-8", errors="ignore")


def read_pdf_file(file_path):
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(file_path))
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text
    except Exception as error:
        print(f"Failed to read PDF {file_path.name}: {error}")
        return ""


def create_chunks(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    text = text.strip()

    if not text:
        return chunks

    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - overlap

    return chunks


def get_all_documents():
    txt_files = sorted(DATA_DIR.rglob("*.txt"))
    pdf_files = sorted(DATA_DIR.rglob("*.pdf"))
    return txt_files + pdf_files


def ingest_documents_into_collection():
    all_files = get_all_documents()

    if not all_files:
        raise FileNotFoundError(
            "No TXT or PDF files were found inside the data folder."
        )

    print(f"\nFound {len(all_files)} document(s) in the data folder.")

    try:
        chroma_client.delete_collection(name=COLLECTION_NAME)
        print("Old knowledge base deleted.")
    except Exception:
        print("Creating a new knowledge base.")

    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)
    chunk_id = 0

    for file_path in all_files:
        print(f"\nProcessing: {file_path.name}")

        if file_path.suffix.lower() == ".txt":
            text = read_txt_file(file_path)
        elif file_path.suffix.lower() == ".pdf":
            text = read_pdf_file(file_path)
        else:
            continue

        if not text.strip():
            print("No readable text found. Skipping file.")
            continue

        chunks = create_chunks(text)
        print(f"Chunks created: {len(chunks)}")

        if not chunks:
            continue

        print("Creating embeddings...")
        embeddings = embedding_model.encode(chunks, show_progress_bar=False)

        print("Storing in ChromaDB...")

        for index, chunk in enumerate(chunks):
            metadata = {
                "source": file_path.name,
                "chunk_number": index + 1,
                "file_type": file_path.suffix.lower(),
            }

            collection.add(
                ids=[f"chunk_{chunk_id}"],
                documents=[chunk],
                embeddings=[embeddings[index].tolist()],
                metadatas=[metadata],
            )
            chunk_id += 1

    print("\n" + "=" * 60)
    print("ALL DOCUMENTS INGESTED SUCCESSFULLY!")
    print(f"Total chunks stored: {chunk_id}")
    print("=" * 60)
    print(f"\nDatabase saved at:\n{DB_PATH}")
    return collection


try:
    collection = chroma_client.get_collection(name=COLLECTION_NAME)
    if collection.count() == 0:
        print("\nKnowledge base is empty.")
        collection = ingest_documents_into_collection()
except Exception:
    print("\nKnowledge base not found.")
    print("Loading documents from the data folder...")
    collection = ingest_documents_into_collection()

print("\nConnected to CivicGuide knowledge base!")
print(f"Total stored chunks: {collection.count()}")

# ==================================================
# CREATE COHERE CLIENT
# ==================================================

try:
    cohere_client = cohere.ClientV2(api_key=COHERE_API_KEY)
except Exception as error:
    print("\nError: Could not initialize the Cohere client.")
    print(f"Details: {error}")
    raise SystemExit(1)

# ==================================================
# EXTRACT TEXT FROM COHERE RESPONSE
# ==================================================

def extract_text(content):
    if not content:
        return ""

    text_parts = []

    for item in content:
        if hasattr(item, "text"):
            item_text = getattr(item, "text", "")
            if item_text:
                text_parts.append(str(item_text))
        elif isinstance(item, dict):
            item_text = item.get("text", "")
            if item_text:
                text_parts.append(str(item_text))

    return "\n".join(text_parts).strip()


# ==================================================
# CHECK NOT FOUND RESPONSE
# ==================================================

def is_not_found_response(answer):
    if not answer:
        return False

    answer = answer.lower().strip()
    not_found_phrases = [
        "i could not find this information",
        "i could not find relevant information",
        "information is not available",
        "not available in the context",
    ]

    return any(phrase in answer for phrase in not_found_phrases)


# ==================================================
# RETRIEVE DOCUMENTS
# ==================================================

def retrieve_documents(question):
    question_embedding = embedding_model.encode(question)
    results = collection.query(
        query_embeddings=[question_embedding.tolist()],
        n_results=TOP_K_RESULTS,
        include=["documents", "metadatas", "distances"],
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    return documents, metadatas, distances


# ==================================================
# BUILD CONTEXT
# ==================================================

def build_context(documents, metadatas):
    context_parts = []

    for index, document in enumerate(documents):
        if index < len(metadatas) and isinstance(metadatas[index], dict):
            metadata = metadatas[index]
            source = metadata.get("source", "Unknown source")
            chunk_number = metadata.get("chunk_number", "Unknown")
        else:
            source = "Unknown source"
            chunk_number = "Unknown"

        context_parts.append(
            f"[Source: {source} | Chunk: {chunk_number}]\n{document}"
        )

    return "\n\n".join(context_parts)


# ==================================================
# GENERATE ANSWER USING COHERE
# ==================================================

def generate_answer(question, context):
    augmented_prompt = f"""
You are CivicGuide AI, an intelligent assistant
for civic and government service information.

Your job is to answer the user's question using
ONLY the information provided in the CONTEXT.

IMPORTANT RULES:

1. Carefully read ALL parts of the context.
2. Use ALL relevant information from the context.
3. Give a COMPLETE answer.
4. Do not unnecessarily shorten important details.
5. If the context contains multiple requirements,
   conditions, steps, documents, benefits, dates,
   categories, or procedures, include all relevant
   information.
6. Do not use outside knowledge.
7. Do not invent information.
8. Do not assume information that is missing.
9. If only part of the answer is available,
   provide that available information clearly.
10. Only say information cannot be found when the
    context genuinely does not contain relevant
    information.

CONTEXT:
{context}

USER QUESTION:
{question}

Provide the most complete and detailed answer possible
using only the context above.
"""

    response = cohere_client.chat(
        model=COHERE_MODEL,
        messages=[{"role": "user", "content": augmented_prompt}],
    )

    return extract_text(response.message.content)


# ==================================================
# PRINT SOURCES
# ==================================================

def print_sources(metadatas):
    print("\nSources:")
    shown_sources = set()

    for metadata in metadatas:
        if not isinstance(metadata, dict):
            continue

        source = metadata.get("source", "Unknown source")
        chunk_number = metadata.get("chunk_number", "Unknown")
        source_info = f"{source} (Chunk {chunk_number})"

        if source_info not in shown_sources:
            print(f"- {source_info}")
            shown_sources.add(source_info)


# ==================================================
# START CHATBOT
# ==================================================

print("\n" + "=" * 60)
print("CIVICGUIDE AI IS READY!")
print("=" * 60)
print("Type 'exit' to stop the program.\n")

while True:
    try:
        question = input("Ask CivicGuide: ")
    except KeyboardInterrupt:
        print("\n\nCivicGuide AI stopped.")
        break
    except EOFError:
        print("\n\nCivicGuide AI stopped.")
        break

    if question.lower().strip() == "exit":
        print("\nThank you for using CivicGuide AI!")
        break

    if not question.strip():
        print("\nPlease enter a question.\n")
        continue

    try:
        print("\nSearching for relevant information...")
        retrieved_documents, retrieved_metadata, distances = retrieve_documents(question)
    except Exception as error:
        print("\nError while searching the knowledge base.")
        print(f"Details: {error}\n")
        continue

    if not retrieved_documents:
        print("\n" + "=" * 60)
        print("CivicGuide AI Answer:")
        print("=" * 60)
        print("I could not find relevant information in the available documents.")
        print()
        continue

    best_distance = distances[0] if distances else float("inf")
    print(f"Best match distance: {best_distance:.4f}")

    if best_distance > DISTANCE_THRESHOLD:
        print("\n" + "=" * 60)
        print("CivicGuide AI Answer:")
        print("=" * 60)
        print("I could not find sufficiently relevant information for this question in the available documents.")
        print()
        continue

    context = build_context(retrieved_documents, retrieved_metadata)
    print("Generating complete answer...")

    try:
        answer = generate_answer(question, context)
    except Exception as error:
        error_message = str(error)
        print("\n" + "=" * 60)
        print("CivicGuide AI Answer:")
        print("=" * 60)

        if (
            "429" in error_message
            or "rate limit" in error_message.lower()
            or "quota" in error_message.lower()
            or "too many requests" in error_message.lower()
        ):
            print("The Cohere AI generation service is temporarily unavailable because the rate limit or quota has been reached.")
            print("\nDocument retrieval is working correctly.")
            print("Please try again later.")
        elif (
            "401" in error_message
            or "403" in error_message
            or "authentication" in error_message.lower()
            or "api key" in error_message.lower()
            or "unauthorized" in error_message.lower()
        ):
            print("There is a problem with the Cohere API key.")
            print("\nPlease check the COHERE_API_KEY value in your .env file.")
        else:
            print("An error occurred while generating the answer.")
            print("\nThe documents were retrieved successfully, but Cohere could not generate a response.")
            print(f"\nError details:\n{error_message}")

        print()
        continue

    if not answer.strip():
        answer = "The AI service did not return an answer. Please try again."

    if is_not_found_response(answer):
        retry_prompt = f"""
You are CivicGuide AI.

The following context was retrieved from the
knowledge base.

Use ALL relevant information in this context
to answer the user's question.

Do not say that information is unavailable
if relevant information exists in the context.

Do not use outside knowledge.

CONTEXT:
{context}

QUESTION:
{question}

Provide a complete answer using the available context.
"""

        try:
            retry_response = cohere_client.chat(
                model=COHERE_MODEL,
                messages=[{"role": "user", "content": retry_prompt}],
            )
            retry_answer = extract_text(retry_response.message.content)
            if retry_answer.strip():
                answer = retry_answer
        except Exception:
            pass

    print("\n" + "=" * 60)
    print("CivicGuide AI Answer:")
    print("=" * 60)
    print(answer)
    print_sources(retrieved_metadata)
    print()
