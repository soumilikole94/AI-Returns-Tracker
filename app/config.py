import os
from dotenv import load_dotenv

# Load variables from .env file into environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set. Please add it to your .env file.")
