
import os
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
APP_NAME = os.getenv("APP_NAME", "AI Interview Coach API")
APP_ENV = os.getenv("APP_ENV", "development")
