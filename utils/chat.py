import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use the latest available model
model = genai.GenerativeModel("gemini-2.0-flash")

def chat_with_ai(user_input: str) -> str:
    """
    Sends user input to Gemini and returns the model's text response.
    """
    prompt_text = (
        f"You are a kind, supportive AI companion focused on mental well-being.\n"
        f"User: {user_input}"
    )

    try:
        response = model.generate_content(prompt_text)

        # ✅ Safely extract text from the response
        if response and response.candidates:
            parts = response.candidates[0].content.parts
            if parts and hasattr(parts[0], "text"):
                return parts[0].text.strip()

        return "MindHaven: Sorry, I could not generate a response."

    except Exception as e:
        return f"MindHaven: Gemini call failed — {str(e)}"

