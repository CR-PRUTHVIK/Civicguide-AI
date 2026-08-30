from pathlib import Path


# Load the document
file_path = Path("data/civic_services.txt")
text = file_path.read_text(encoding="utf-8")


# Function to split text into chunks
def create_chunks(text, chunk_size=300):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks


# Create chunks
chunks = create_chunks(text)


# Print the chunks
for index, chunk in enumerate(chunks, start=1):
    print(f"\n{'=' * 50}")
    print(f"CHUNK {index}")
    print('=' * 50)
    print(chunk)