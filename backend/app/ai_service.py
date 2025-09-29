from typing import Optional, Tuple
import json
import re
from google import genai
from .config import GEMINI_API_KEY

# Pick one of YOUR working models from list_models.py
# You confirmed this works already:
DEFAULT_MODEL = "models/gemini-2.5-flash"

SYSTEM_RUBRIC = """
You are an Interview Coach. Evaluate answers using the STAR method (Situation, Task, Action, Result) and these criteria:
- Relevance: Does the answer address the specific question?
- Structure (STAR): Is there clear Situation, Task, Action, Result?
- Technical depth: Specifics, tradeoffs, correctness (for technical questions).
- Communication: Clarity, conciseness, and confident tone.

Scoring: Provide an overall score from 1.0 to 5.0 (inclusive, decimals allowed).
Feedback style: short, actionable bullets (<=120 words total).
Output STRICT JSON ONLY with this schema:
{
  "feedback": "string",
  "score": number
}
No extra keys. No markdown. No comments. JSON only.
"""

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

    def evaluate_answer(self, question: str, user_answer: str) -> Tuple[str, float]:
        """
        Returns (feedback, score) using a strict JSON contract.
        Falls back to best-effort JSON parsing if the model adds noise.
        """
        prompt = f"""{SYSTEM_RUBRIC}

Question:
{question}

Candidate Answer:
{user_answer}

Return JSON only.
"""
        resp = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        raw = getattr(resp, "text", "").strip()

        # Try strict JSON parse first
        parsed = self._safe_json(raw)
        if parsed and "feedback" in parsed and "score" in parsed:
            fb = str(parsed["feedback"]).strip()
            try:
                sc = float(parsed["score"])
            except Exception:
                sc = 0.0
            # clamp score 1..5
            sc = max(1.0, min(5.0, sc))
            return fb, sc

        # If parsing failed, return raw text as feedback and neutral score
        return raw[:800], 3.0

    @staticmethod
    def _safe_json(text: str) -> Optional[dict]:
        # Extract the largest JSON object from the text if any
        try:
            return json.loads(text)
        except Exception:
            pass
        try:
            # naive brace capture
            match = re.search(r"\{.*\}", text, flags=re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception:
            pass
        return None
