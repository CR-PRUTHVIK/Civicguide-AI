import os

from dotenv import load_dotenv
import cohere


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# GET COHERE API KEY
# ==========================================

api_key = os.getenv("COHERE_API_KEY")


if not api_key:
    raise ValueError(
        "COHERE_API_KEY not found. "
        "Please add your Cohere API key to the .env file."
    )


# ==========================================
# CREATE COHERE CLIENT
# ==========================================

client = cohere.ClientV2(
    api_key=api_key
)


# ==========================================
# EXTRACT TEXT FROM COHERE RESPONSE
# ==========================================

def extract_text(content):

    if not content:
        return ""


    text_parts = []


    for content_item in content:

        # Cohere object response
        if hasattr(content_item, "text"):

            text = getattr(
                content_item,
                "text",
                ""
            )

            if text:
                text_parts.append(
                    str(text)
                )


        # Dictionary response
        elif isinstance(content_item, dict):

            item_type = content_item.get(
                "type"
            )

            item_text = content_item.get(
                "text",
                ""
            )


            if item_type == "text" and item_text:

                text_parts.append(
                    str(item_text)
                )


    return "\n".join(
        text_parts
    ).strip()


# ==========================================
# GENERATE ANSWER
# ==========================================

def generate_answer(question, context):

    # Check if context exists
    if not context or not str(context).strip():

        return (
            "I could not find this information "
            "in the available documents."
        )


    # ==========================================
    # BUILD DYNAMIC RAG PROMPT
    # ==========================================

    augmented_prompt = f"""You are CivicGuide AI, an intelligent, professional government services and civic assistance information guide.

Your job is to answer the user's question clearly, accurately, and comprehensively based on the official CONTEXT provided below.

INSTRUCTIONS:
1. Synthesize a direct, helpful, and well-structured answer using the information in the context.
2. Format your response cleanly using Markdown (use bold headings, bullet points, and numbered steps where appropriate).
3. Be comprehensive: include all relevant eligibility requirements, document checklists, application steps, and official portal advice found in the context.
4. Do not invent facts or use outside knowledge not supported by the context.
5. If the context does not contain enough relevant information to answer the question, politely explain:
   "I could not find sufficient information regarding this topic in the available documents. Please verify with official government channels or ask about voter services, scholarships, certificates, or civic grievance procedures."

CONTEXT:
{context}

USER QUESTION:
{question}

Synthesize a clear, detailed, and nicely formatted answer:"""


    try:

        # ==========================================
        # SEND REQUEST TO COHERE
        # ==========================================

        response = client.chat(

            model="command-r-08-2024",

            messages=[
                {
                    "role": "user",
                    "content": augmented_prompt
                }
            ]

        )


        # ==========================================
        # EXTRACT ANSWER
        # ==========================================

        answer = extract_text(
            response.message.content
        )


        # ==========================================
        # CHECK EMPTY RESPONSE
        # ==========================================

        if not answer:

            return (
                "The AI service did not return "
                "an answer. Please try again."
            )


        # ==========================================
        # RETURN ANSWER TO API
        # ==========================================

        return answer


    except Exception as error:

        error_message = str(error)


        print(
            f"Cohere generation error: "
            f"{error_message}"
        )


        # Rate limit / quota error
        if (

            "429" in error_message

            or "rate limit"
            in error_message.lower()

            or "quota"
            in error_message.lower()

            or "too many requests"
            in error_message.lower()

        ):

            return (
                "The AI generation service is temporarily "
                "unavailable because the API quota or rate "
                "limit has been reached. Please try again later."
            )


        # Authentication error
        elif (

            "401" in error_message

            or "403" in error_message

            or "authentication"
            in error_message.lower()

            or "api key"
            in error_message.lower()

            or "unauthorized"
            in error_message.lower()

        ):

            return (
                "There is a problem with the Cohere API key "
                "or authentication."
            )


        # General error
        else:

            return (
                "An error occurred while generating "
                "the answer. Please try again."
            )