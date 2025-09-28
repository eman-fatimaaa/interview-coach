
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ..ai_service import GeminiClient

router = APIRouter(prefix="/ai", tags=["ai"])
gc = GeminiClient()

class PingRequest(BaseModel):
    prompt: str = Field(..., example="Say hello in a friendly way.")

class PingResponse(BaseModel):
    reply: str

@router.post("/ping", response_model=PingResponse)
def ai_ping(req: PingRequest):
    try:
        reply = gc.generate_text(req.prompt)
        return PingResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {e}")
