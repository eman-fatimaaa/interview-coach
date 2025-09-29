from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..deps import get_current_user
from ..models import User, InterviewSession, Attempt

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users")
def all_users(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403, "Admins only")
    users = session.exec(select(User)).all()
    return [u.model_dump() for u in users]

@router.get("/users/{user_id}/sessions")
def user_sessions(user_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403, "Admins only")
    sessions = session.exec(select(InterviewSession).where(InterviewSession.user_id == user_id)).all()
    return [s.model_dump() for s in sessions]

@router.get("/sessions/{session_id}/attempts")
def session_attempts(session_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403, "Admins only")
    atts = session.exec(select(Attempt).where(Attempt.session_id == session_id)).all()
    return [a.model_dump() for a in atts]
