from google import genai
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Get API key from .env
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)


def answer_question_with_gemini(question: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=question
        )

        return response.text.strip()

    except Exception as e:
        return f"⚠️ Error in QnA: {e}"