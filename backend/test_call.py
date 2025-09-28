from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

print("Trying Gemini 1.5 Flash (new endpoint)...")
resp = client.models.generate_content(
    model="models/gemini-1.5-flash",
    contents="Say hello in one short sentence."
)
print(resp.text)
