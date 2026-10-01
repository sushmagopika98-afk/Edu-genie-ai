
from google import genai
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Set up Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def get_learning_recommendations(topic):
    prompt = f"""
You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics,
order of learning, and resources.
Include beginner, intermediate, and advanced levels if needed.
"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        if response.text:
            return response.text.strip()
        else:
            return "❌ Could not extract content from Gemini response."

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"❌ Error occurred: {str(e)}"