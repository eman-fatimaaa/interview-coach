from typing import Optional, Tuple, Dict, Any
import json
import re
import time
from google import genai
from .config import GEMINI_API_KEY

DEFAULT_MODEL = "models/gemini-2.5-flash"

RUBRIC_PROMPT = """
You are an Interview Coach. Evaluate the candidate’s answer with this rubric.
Return STRICT JSON only, no markdown, no extra keys.

Rubric criteria (each 1.0 to 5.0):
- relevance
- star_structure    (use of Situation/Task/Action/Result)
- technical_depth   (specifics, tradeoffs, correctness – for technical Qs)
- communication     (clarity, conciseness, confident tone)

Also compute an overall_score (1.0 to 5.0). Keep feedback short, actionable (<= 120 words).

JSON schema EXACTLY:
{
  "feedback": "string",
  "overall_score": number,
  "rubric": {
    "relevance": number,
    "star_structure": number,
    "technical_depth": number,
    "communication": number
  }
}
"""

SUMMARY_PROMPT = """
You are an Interview Coach. You will see a list of Q&A items with per-criterion scores.
Write a concise session summary (<= 180 words) covering strengths, gaps, and 3 specific next-step suggestions.
Return STRICT JSON ONLY:
{
  "summary": "string",
  "strengths": ["string", "string", "string"],
  "improvements": ["string", "string", "string"]
}
"""

def _clamp(x: float, lo=1.0, hi=5.0) -> float:
    try:
        return max(lo, min(hi, float(x)))
    except Exception:
        return lo

class GeminiClient:
    def __init__(self, api_key: Optional[str] = GEMINI_API_KEY, model: str = DEFAULT_MODEL):
        if not api_key:
            raise RuntimeError("Missing GEMINI_API_KEY in .env")
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate_text(self, prompt: str) -> str:
        resp = self.client.models.generate_content(model=self.model, contents=prompt)
        return getattr(resp, "text", "").strip()

    # ---------- NEW: evaluation with retries & strict JSON ----------
    def evaluate_answer(self, question: str, user_answer: str, retries: int = 3, backoff: float = 0.8) -> Dict[str, Any]:
        prompt = f"""{RUBRIC_PROMPT}

Question:
{question}

Candidate Answer:
{user_answer}

Return JSON only.
"""
        err = None
        for i in range(retries):
            try:
                resp = self.client.models.generate_content(model=self.model, contents=prompt)
                raw = getattr(resp, "text", "").strip()
                data = self._safe_json(raw)
                if not data:
                    raise ValueError("Model did not return valid JSON")
                # normalize + clamp
                data["overall_score"] = _clamp(data.get("overall_score", 3.0))
                rub = data.get("rubric", {}) or {}
                data["rubric"] = {
                    "relevance": _clamp(rub.get("relevance", 3.0)),
                    "star_structure": _clamp(rub.get("star_structure", 3.0)),
                    "technical_depth": _clamp(rub.get("technical_depth", 3.0)),
                    "communication": _clamp(rub.get("communication", 3.0)),
                }
                return data
            except Exception as e:
                err = e
                time.sleep(backoff * (2 ** i))
        # fallback if all retries failed
        return {
            "feedback": f"AI evaluation error: {err}",
            "overall_score": 3.0,
            "rubric": {
                "relevance": 3.0,
                "star_structure": 3.0,
                "technical_depth": 3.0,
                "communication": 3.0,
            },
        }

    # ---------- NEW: session summary ----------
    def summarize_session(self, items: list[dict], retries: int = 3, backoff: float = 0.8) -> Dict[str, Any]:
        """
        items: list of {question, answer, overall_score, rubric{...}}
        """
        serialized = json.dumps(items, ensure_ascii=False, indent=2)
        prompt = f"""{SUMMARY_PROMPT}

Data:
{serialized}

Return JSON only.
"""
        err = None
        for i in range(retries):
            try:
                resp = self.client.models.generate_content(model=self.model, contents=prompt)
                raw = getattr(resp, "text", "").strip()
                data = self._safe_json(raw)
                if not data:
                    raise ValueError("Model did not return valid JSON")
                return data
            except Exception as e:
                err = e
                time.sleep(backoff * (2 ** i))
        return {"summary": f"AI summary error: {err}", "strengths": [], "improvements": []}

    @staticmethod
    def _safe_json(text: str) -> Optional[dict]:
        try:
            return json.loads(text)
        except Exception:
            pass
        try:
            import re as _re
            m = _re.search(r"\{.*\}", text, flags=_re.DOTALL)
            if m:
                return json.loads(m.group(0))
        except Exception:
            pass
        return None
