import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb
from dotenv import load_dotenv

# Ensure project root is in Python path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.generation import generate_answer

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Load the CivicGuide document
file_path = BASE_DIR / "data" / "civic_services.txt"
text = file_path.read_text(encoding="utf-8")


# Split text into chunks
def create_chunks(text, chunk_size=300):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
    return chunks


chunks = create_chunks(text)

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings for the chunks
print("Creating embeddings...")
embeddings = model.encode(chunks)

# Create ChromaDB client
client = chromadb.Client()

# Create collection
collection = client.get_or_create_collection(
    name="civicguide_documents"
)

# Add chunks to ChromaDB
for index, chunk in enumerate(chunks):
    collection.add(
        ids=[f"chunk_{index}"],
        documents=[chunk],
        embeddings=[embeddings[index].tolist()]
    )

# Question to ask
question = "Who is eligible for a scholarship?"

# Convert question into embedding
question_embedding = model.encode(question)

# 1. Search the vector database (Retrieval)
results = collection.query(
    query_embeddings=[question_embedding.tolist()],
    n_results=2
)

retrieved_docs = results["documents"][0]

print("\n" + "=" * 60)
print(f"QUESTION: {question}")
print("=" * 60)

print("\n[Step 1: Retrieved Chunks from ChromaDB]")
for i, document in enumerate(retrieved_docs):
    print(f"\n--- Chunk #{i+1} ---")
    print(document)

# 2. Combine chunks into context (Augmentation)
context = "\n\n".join(retrieved_docs)

# 3. Generate natural language answer with Cohere (Generation)
print("\n" + "=" * 60)
print("[Step 2: AI Generated Answer via Cohere LLM]")
print("=" * 60)
answer = generate_answer(question, context)
print(answer)
print("=" * 60)