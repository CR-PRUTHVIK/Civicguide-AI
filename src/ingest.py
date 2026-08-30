from pathlib import Path

import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


# Find the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent


# Data folder
DATA_DIR = BASE_DIR / "data"


# -----------------------------------
# CREATE OVERLAPPING CHUNKS
# -----------------------------------

def create_chunks(text, chunk_size=300, overlap=50):

    chunks = []
    start = 0

    while start < len(text):

        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# -----------------------------------
# READ TXT FILE
# -----------------------------------

def read_txt_file(file_path):

    return file_path.read_text(
        encoding="utf-8"
    )


# -----------------------------------
# READ PDF FILE
# -----------------------------------

def read_pdf_file(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# -----------------------------------
# FIND ALL DOCUMENTS
# -----------------------------------

txt_files = list(DATA_DIR.glob("*.txt"))
pdf_files = list(DATA_DIR.glob("*.pdf"))

all_files = txt_files + pdf_files


if not all_files:

    raise FileNotFoundError(
        "No TXT or PDF files were found inside the data folder."
    )


print(
    f"Found {len(all_files)} document(s).\n"
)


# -----------------------------------
# LOAD EMBEDDING MODEL
# -----------------------------------

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# -----------------------------------
# CONNECT TO CHROMADB
# -----------------------------------

db_path = BASE_DIR / "chroma_db"

client = chromadb.PersistentClient(
    path=str(db_path)
)


# -----------------------------------
# DELETE OLD COLLECTION
# -----------------------------------

try:

    client.delete_collection(
        name="civicguide_documents"
    )

    print("Old knowledge base deleted.")

except Exception:

    print("Creating a new knowledge base.")


# -----------------------------------
# CREATE NEW COLLECTION
# -----------------------------------

collection = client.get_or_create_collection(
    name="civicguide_documents"
)


# -----------------------------------
# PROCESS ALL DOCUMENTS
# -----------------------------------

chunk_id = 0


for file_path in all_files:

    print(
        f"\nProcessing: {file_path.name}"
    )


    # Read TXT file
    if file_path.suffix.lower() == ".txt":

        text = read_txt_file(
            file_path
        )


    # Read PDF file
    elif file_path.suffix.lower() == ".pdf":

        text = read_pdf_file(
            file_path
        )


    # Create chunks
    chunks = create_chunks(text)


    print(
        f"Chunks created: {len(chunks)}"
    )


    # Skip empty documents
    if not chunks:

        print(
            "No readable text found. Skipping file."
        )

        continue


    # Create embeddings
    print(
        "Creating embeddings..."
    )

    embeddings = model.encode(
        chunks
    )


    # Store chunks
    print(
        "Storing in ChromaDB..."
    )


    for index, chunk in enumerate(chunks):

        metadata = {
            "source": file_path.name,
            "chunk_number": index + 1,
            "file_type": file_path.suffix.lower()
        }


        collection.add(
            ids=[
                f"chunk_{chunk_id}"
            ],
            documents=[
                chunk
            ],
            embeddings=[
                embeddings[index].tolist()
            ],
            metadatas=[
                metadata
            ]
        )


        chunk_id += 1


# -----------------------------------
# FINISH
# -----------------------------------

print("\n" + "=" * 50)

print(
    "All documents ingested successfully!"
)

print(
    f"Total chunks stored: {chunk_id}"
)

print("=" * 50)


print(
    f"\nDatabase saved at: {db_path}"
)