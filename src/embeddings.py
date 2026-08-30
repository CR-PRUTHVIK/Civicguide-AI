from sentence_transformers import SentenceTransformer


# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Sample text
text = "Documents required for a caste certificate"


# Convert text into an embedding
embedding = model.encode(text)


print("Text:")
print(text)

print("\nEmbedding:")
print(embedding)

print("\nNumber of values in embedding:")
print(len(embedding))