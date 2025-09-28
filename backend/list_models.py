from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

print("Available models for your key:\n")
for m in client.models.list():
    print("-", m.name)
