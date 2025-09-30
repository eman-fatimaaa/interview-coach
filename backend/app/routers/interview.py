from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
from datetime import datetime
import json

from ..database import get_session
from ..deps import get_current_user
from ..models import User, InterviewSession, InterviewScenario, Question, Attempt
from ..ai_service import GeminiClient
from ..ratelimit import ensure_rate

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
    rubric: Optional[Dict[str, float]] = None

    class Config:
        from_attributes = True

class SessionSummaryOut(BaseModel):
    session_id: int
    started_at: datetime
    ended_at: Optional[datetime]
    average_scores: Dict[str, float]
    summary: str
    strengths: List[str]
    improvements: List[str]

# --------- Helpers ---------
def _extract_rubric(attempt: Attempt) -> Optional[Dict[str, float]]:
    try:
        data = json.loads(attempt.ai_feedback or "")
        rub = data.get("rubric")
        if isinstance(rub, dict):
            keys = ["relevance", "star_structure", "technical_depth", "communication"]
            return {k: float(rub.get(k, 0.0)) for k in keys}
    except Exception:
        pass
    return None

# --------- Endpoints ---------
@router.post("/sessions/start", response_model=SessionOut)
def start_session(
    body: StartSessionIn,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    scenario = session.get(InterviewScenario, body.scenario_id)
    if not scenario:
        raise HTTPException(404, "Scenario not found")
    sess = InterviewSession(user_id=user.id, scenario_id=scenario.id, status="active")
    session.add(sess)
    session.commit()
    session.refresh(sess)
    return sess

@router.get("/sessions/me", response_model=List[SessionOut])
def my_sessions(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return session.exec(
        select(InterviewSession)
        .where(InterviewSession.user_id == user.id)
        .order_by(InterviewSession.started_at.desc())
    ).all()

@router.post("/answer", response_model=AttemptOut)
def submit_answer(
    body: AnswerIn,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    # Rate limit (AI call)
    ensure_rate(user.id)

    # Validate session & ownership
    sess = session.get(InterviewSession, body.session_id)
    if not sess or sess.user_id != user.id:
        raise HTTPException(404, "Session not found")
    if sess.status != "active":
        raise HTTPException(400, "Session is not active")

    # Validate question in scenario
    q = session.get(Question, body.question_id)
    if not q or q.scenario_id != sess.scenario_id:
        raise HTTPException(400, "Question does not belong to session's scenario")

    # Create attempt
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

    # Evaluate with Gemini
    data = gc.evaluate_answer(q.text, body.answer.strip())
    attempt.ai_feedback = json.dumps(data, ensure_ascii=False)
    attempt.score = float(data.get("overall_score", 3.0))
    session.add(attempt)
    session.commit()
    session.refresh(attempt)

    return AttemptOut(**attempt.model_dump(), rubric=data.get("rubric"))

@router.get("/attempts/me", response_model=List[AttemptOut])
def my_attempts(
    session_id: Optional[int] = None,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    stmt = (
        select(Attempt)
        .where(Attempt.user_id == user.id)
        .order_by(Attempt.created_at.desc())
    )
    if session_id:
        stmt = stmt.where(Attempt.session_id == session_id)
    rows = session.exec(stmt).all()
    return [AttemptOut(**a.model_dump(), rubric=_extract_rubric(a)) for a in rows]

@router.post("/sessions/{session_id}/complete", response_model=SessionOut)
def complete_session(
    session_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    sess = session.get(InterviewSession, session_id)
    if not sess or sess.user_id != user.id:
        raise HTTPException(404, "Session not found")
    sess.status = "completed"
    sess.ended_at = datetime.utcnow()
    session.add(sess)
    session.commit()
    session.refresh(sess)
    return sess

@router.get("/sessions/{session_id}/summary", response_model=SessionSummaryOut)
def session_summary(
    session_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    sess = session.get(InterviewSession, session_id)
    if not sess or sess.user_id != user.id:
        raise HTTPException(404, "Session not found")

    atts = session.exec(
        select(Attempt).where(Attempt.session_id == sess.id).order_by(Attempt.created_at.asc())
    ).all()
    if not atts:
        raise HTTPException(400, "No attempts in this session")

    items = []
    agg = {"relevance": 0.0, "star_structure": 0.0, "technical_depth": 0.0, "communication": 0.0}
    n = 0
    for a in atts:
        q = session.get(Question, a.question_id)
        rub = _extract_rubric(a) or {}
        items.append({
            "question": q.text if q else f"Q#{a.question_id}",
            "answer": a.user_answer,
            "overall_score": float(a.score or 0.0),
            "rubric": rub,
        })
        if rub:
            for k in agg:
                agg[k] += float(rub.get(k, 0.0))
            n += 1

    avg = {k: (round(v / n, 2) if n else 0.0) for k, v in agg.items()}
    report = gc.summarize_session(items)

    return SessionSummaryOut(
    session_id=sess.id,
    started_at=sess.started_at,
    ended_at=sess.ended_at,
    average_scores=avg,
    summary=report.get("summary", ""),
    strengths=report.get("strengths", []),
    improvements=report.get("improvements", []),
)


# --------- NEW: Session details (with questions) ---------
@router.get("/sessions/{session_id}/details")
def session_details(
    session_id: int,
    db: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    sess = db.get(InterviewSession, session_id)
    if not sess or sess.user_id != user.id:
        raise HTTPException(404, "Session not found")

    scenario = db.get(InterviewScenario, sess.scenario_id)
    if not scenario:
        raise HTTPException(404, "Scenario not found")

    questions = db.exec(
        select(Question).where(Question.scenario_id == scenario.id)
    ).all()

    return {
        "session": {
            "id": sess.id,
            "scenario_id": sess.scenario_id,
            "status": sess.status,
            "started_at": sess.started_at,
            "ended_at": sess.ended_at,
        },
        "questions": [
            {"id": q.id, "text": q.text, "difficulty": q.difficulty}
            for q in questions
        ],
    }


# --------- NEW: Delete Session ---------
@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    sess = session.get(InterviewSession, session_id)
    if not sess or sess.user_id != user.id:
        raise HTTPException(404, "Session not found")

    # Delete attempts first (foreign key constraint)
    attempts = session.exec(select(Attempt).where(Attempt.session_id == sess.id)).all()
    for a in attempts:
        session.delete(a)

    # Delete the session
    session.delete(sess)
    session.commit()
    return None
