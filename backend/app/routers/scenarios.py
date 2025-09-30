from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select

from ..database import get_session         
from ..deps import get_current_user, require_admin
from ..models import InterviewScenario, Question, User

router = APIRouter(prefix="/scenarios", tags=["scenarios"])

# ---------- Response models ----------
class ScenarioOut(BaseModel):
    id: int
    title: str
    role: str
    level: str
    description: str

    class Config:
        from_attributes = True

class QuestionOut(BaseModel):
    id: int
    scenario_id: int
    text: str
    difficulty: str

    class Config:
        from_attributes = True

# ---------- Endpoints ----------
@router.get("", response_model=List[ScenarioOut])
def list_scenarios(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return session.exec(select(InterviewScenario)).all()

@router.get("/{scenario_id}/questions", response_model=List[QuestionOut])
def list_questions(
    scenario_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    scenario = session.get(InterviewScenario, scenario_id)
    if not scenario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")
    return session.exec(select(Question).where(Question.scenario_id == scenario_id)).all()

# Seed demo data (admin only)
@router.post("/seed")
def seed_scenarios(
    session: Session = Depends(get_session),
    _: User = Depends(require_admin), 
):
    # idempotent-ish seed: if any scenarios exist, skip
    exists = session.exec(select(InterviewScenario)).first()
    if exists:
        count = session.exec(select(InterviewScenario)).all()
        return {"message": "Scenarios already seeded", "count": len(count)}

    s1 = InterviewScenario(
        title="Backend Engineer Interview",
        role="Backend",
        level="Junior",
        description="Covers APIs, databases, HTTP, and Python basics.",
    )
    s2 = InterviewScenario(
        title="Frontend Engineer Interview",
        role="Frontend",
        level="Junior",
        description="Covers Vue.js, HTML/CSS, and web fundamentals.",
    )
    session.add(s1)
    session.add(s2)
    session.commit()
    session.refresh(s1)
    session.refresh(s2)

    q = [
        Question(scenario_id=s1.id, text="Explain REST vs. GraphQL.", difficulty="medium"),
        Question(scenario_id=s1.id, text="Design a rate limiter for an API.", difficulty="hard"),
        Question(scenario_id=s1.id, text="Describe transactions and isolation levels.", difficulty="hard"),
        Question(scenario_id=s2.id, text="What is the Virtual DOM in Vue?", difficulty="easy"),
        Question(scenario_id=s2.id, text="How do you manage state across components?", difficulty="medium"),
        Question(scenario_id=s2.id, text="Explain hydration in SSR frameworks.", difficulty="hard"),
    ]
    session.add_all(q)
    session.commit()

    return {"message": "Seeded demo scenarios & questions", "scenario_ids": [s1.id, s2.id]}
