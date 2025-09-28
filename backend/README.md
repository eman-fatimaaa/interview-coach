
# Backend (FastAPI)

## Prereqs
- Python 3.10+

## Setup
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Put your GEMINI_API_KEY in .env
uvicorn app.main:app --reload --port 8000
```

## Test
- Open http://localhost:8000/health  → `{"status":"ok"}`
- POST http://localhost:8000/ai/ping with JSON: `{"prompt":"Say hello"}`
