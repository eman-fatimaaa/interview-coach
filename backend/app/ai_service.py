from typing import Optional, Dict, Any
import json, time, re
import google.generativeai as genai
from .config import GEMINI_API_KEY

DEFAULT_MODEL = "gemini-2.0-flash"   

genai.configure(api_key=GEMINI_API_KEY)


def _clamp(x: float, lo=1.0, hi=5.0) -> float:
    try:
        return max(lo, min(hi, float(x)))
    except Exception:
        return lo


class GeminiClient:
    def __init__(self, model: str = DEFAULT_MODEL):
        if not GEMINI_API_KEY:
            raise RuntimeError("Missing GEMINI_API_KEY in .env")
        self.model = genai.GenerativeModel(model)

    def generate_text(self, prompt: str) -> str:
        resp = self.model.generate_content(prompt)
        return getattr(resp, "text", "").strip()

    def evaluate_answer(self, question: str, user_answer: str, retries: int = 3, backoff: float = 0.8) -> Dict[str, Any]:
        prompt = f"""You are an Interview Coach. Evaluate the candidate’s answer...

Question:
{question}

Candidate Answer:
{user_answer}

Return JSON only.
"""
        err = None
        for i in range(retries):
            try:
                resp = self.model.generate_content(prompt)
                raw = getattr(resp, "text", "").strip()
                data = self._safe_json(raw)
                if not data:
                    raise ValueError("Model did not return valid JSON")
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
        return {
            "feedback": f"AI evaluation error: {err}",
            "overall_score": 3.0,
            "rubric": {k: 3.0 for k in ["relevance","star_structure","technical_depth","communication"]}
        }

    def summarize_session(self, items: list[dict], retries: int = 3, backoff: float = 0.8) -> Dict[str, Any]:
        serialized = json.dumps(items, ensure_ascii=False, indent=2)
        prompt = f"""You are an Interview Coach. Summarize this session...

Data:
{serialized}

Return JSON only.
"""
        err = None
        for i in range(retries):
            try:
                resp = self.model.generate_content(prompt)
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
    def _safe_json(text: str):
        try:
            return json.loads(text)
        except Exception:
            m = re.search(r"\{.*\}", text, flags=re.DOTALL)
            if m:
                return json.loads(m.group(0))
        return None
