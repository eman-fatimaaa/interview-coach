from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime

from ..database import get_session
from ..deps import get_current_user
from ..models import User, InterviewSession, InterviewScenario, Question, Attempt
from ..ai_service import GeminiClient

router = APIRouter(prefix="/interview", tags=["interview"])
gc = GeminiClient()

# --------- Schemas ---------
class StartSessionIn(BaseModel):
    scenario_id: int = Field(..., gt=0)

class SessionOut(BaseModel):
    id: int
    scenario_id: int
    status: str
    started_at: datetime
    ended_at: Optional[datetime]
    class Config:
        from_attributes = True

class AnswerIn(BaseModel):
    session_id: int
    question_id: int
    answer: str = Field(..., min_length=2)

class AttemptOut(BaseModel):
    id: int
    session_id: int
    user_id: int
    question_id: int
    user_answer: str
    ai_feedback: Optional[str]
    score: Optional[float]
    created_at: datetime
    class Config:
        from_attributes = True

# --------- Endpoints ---------
@router.post("/sessions/start", response_model=SessionOut)
def start_session(body: StartSessionIn, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    scenario = session.get(InterviewScenario, body.scenario_id)
    if not scenario:
        raise HTTPException(404, "Scenario not found")
    sess = InterviewSession(user_id=user.id, scenario_id=scenario.id, status="active")
    session.add(sess)
    session.commit()
    session.refresh(sess)
    return sess

@router.get("/sessions/me", response_model=List[SessionOut])
def my_sessions(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    rows = session.exec(select(InterviewSession).where(InterviewSession.user_id == user.id).order_by(InterviewSession.started_at.desc())).all()
    return rows

@router.post("/answer", response_model=AttemptOut)
def submit_answer(body: AnswerIn, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    # Validate session belongs to user & is active
    sess = session.get(InterviewSession, body.session_id)
    if not sess or sess.user_id != user.id:
        raise HTTPException(404, "Session not found")
    if sess.status != "active":
        raise HTTPException(400, "Session is not active")

    # Validate question belongs to scenario
    q = session.get(Question, body.question_id)
    if not q or q.scenario_id != sess.scenario_id:
        raise HTTPException(400, "Question does not belong to session's scenario")

    # 1) Store raw attempt first
    attempt = Attempt(
        session_id=sess.id,
        user_id=user.id,
        question_id=q.id,
        user_answer=body.answer.strip(),
        ai_feedback=None,
        score=None,
    )
    session.add(attempt)
    session.commit()
    session.refresh(attempt)

    # 2) Ask Gemini to evaluate
    try:
        feedback, score = gc.evaluate_answer(q.text, body.answer.strip())
    except Exception as e:
        # If AI fails, keep attempt without feedback/score
        feedback, score = (f"AI evaluation error: {e}", None)

    # 3) Update attempt with AI results
    attempt.ai_feedback = feedback
    attempt.score = score
    session.add(attempt)
    session.commit()
    session.refresh(attempt)
    return attempt

@router.get("/attempts/me", response_model=List[AttemptOut])
def my_attempts(session_id: Optional[int] = None, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    stmt = select(Attempt).where(Attempt.user_id == user.id).order_by(Attempt.created_at.desc())
    if session_id:
        stmt = stmt.where(Attempt.session_id == session_id)
    rows = session.exec(stmt).all()
    return rows

@router.post("/sessions/{session_id}/complete", response_model=SessionOut)
def complete_session(session_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    sess = session.get(InterviewSession, session_id)
    if not sess or sess.user_id != user.id:
        raise HTTPException(404, "Session not found")
    sess.status = "completed"
    sess.ended_at = datetime.utcnow()
    session.add(sess)
    session.commit()
    session.refresh(sess)
    return sess
