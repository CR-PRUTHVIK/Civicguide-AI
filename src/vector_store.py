from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb


# Load the CivicGuide document
file_path = Path("data/civic_services.txt")
text = file_path.read_text(encoding="utf-8")


# Split the text into chunks
def create_chunks(text, chunk_size=300):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks


chunks = create_chunks(text)

print(f"Total chunks created: {len(chunks)}")


# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")


# Create embeddings for all chunks
print("Creating embeddings...")
embeddings = model.encode(chunks)

print(f"Embeddings created: {len(embeddings)}")


# Create ChromaDB client
client = chromadb.Client()


# Create a collection
collection = client.get_or_create_collection(
    name="civicguide_documents"
)


# Store chunks and embeddings
for index, chunk in enumerate(chunks):

    collection.add(
        ids=[f"chunk_{index}"],
        documents=[chunk],
        embeddings=[embeddings[index].tolist()]
    )


print("All chunks stored successfully in ChromaDB!")