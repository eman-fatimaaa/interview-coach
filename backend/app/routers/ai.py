from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from ..ai_service import GeminiClient
from ..deps import get_current_user
from ..models import User

router = APIRouter(prefix="/ai", tags=["ai"])
gc = GeminiClient()

class PingRequest(BaseModel):
    prompt: str = Field(..., example="Say hello in a friendly way.")

class PingResponse(BaseModel):
    reply: str

@router.post("/ping", response_model=PingResponse)
def ai_ping(req: PingRequest, user: User = Depends(get_current_user)):
    try:
        reply = gc.generate_text(req.prompt)
        return PingResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {e}")
