from typing import Optional
from google import genai
from .config import GEMINI_API_KEY

# Pick one of the models from your list
DEFAULT_MODEL = "models/gemini-2.5-flash"

class GeminiClient:
    def __init__(self, api_key: Optional[str] = GEMINI_API_KEY, model: str = DEFAULT_MODEL):
        if not api_key:
            raise RuntimeError("Missing GEMINI_API_KEY in .env")
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate_text(self, prompt: str) -> str:
        resp = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return getattr(resp, "text", "").strip()


