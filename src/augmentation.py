import sys
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.generation import generate_answer

load_dotenv(BASE_DIR / ".env")

# Retrieved information from the retriever
retrieved_documents = [
    """
Scholarship

Government scholarships may provide financial assistance to eligible students.

Eligibility:
Eligibility requirements can depend on factors such as educational status,
family income, category, and the specific scholarship scheme.
""",
    """
Required Documents:
Applicants may be required to provide identity documents,
educational records, income-related documents,
and other scheme-specific documents.
"""
]

# User question
question = "Who is eligible for a scholarship?"

# Combine retrieved documents into one context (Augmentation)
context = "\n\n".join(retrieved_documents)

# Create the augmented prompt
augmented_prompt = f"""
You are CivicGuide AI.

Answer the user's question using ONLY the information provided in the context.

If the answer is not available in the context, say:
"I could not find this information in the available government documents."

CONTEXT:
{context}

QUESTION:
{question}
"""

print("=" * 60)
print("AUGMENTED PROMPT SENT TO LLM:")
print("=" * 60)
print(augmented_prompt)

print("=" * 60)
print("GENERATED ANSWER FROM COHERE:")
print("=" * 60)
answer = generate_answer(question, context)
print(answer)
print("=" * 60)