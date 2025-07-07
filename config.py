import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")  # Default Groq model

def check_api_key():
    """Checks if the Groq API key is set."""
    if not GROQ_API_KEY:
        print("Error: GROQ_API_KEY not found in environment or .env file.")
        print("Please set GROQ_API_KEY in your environment or .env file.")
        exit()

check_api_key()
