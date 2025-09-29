from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, UniqueConstraint, Relationship

# ---- Existing User model (unchanged) ----
class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password_hash: str
    role: str = Field(default="user")

    sessions: List["InterviewSession"] = Relationship(back_populates="user")
    attempts: List["Attempt"] = Relationship(back_populates="user")

# ---- New Interview domain models ----
class InterviewScenario(SQLModel, table=True):
    __tablename__ = "interview_scenarios"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    role: str  # e.g., "Backend Engineer"
    level: str  # e.g., "Junior", "Mid", "Senior"
    description: str = ""

    questions: List["Question"] = Relationship(back_populates="scenario")
    sessions: List["InterviewSession"] = Relationship(back_populates="scenario")

class Question(SQLModel, table=True):
    __tablename__ = "questions"
    id: Optional[int] = Field(default=None, primary_key=True)
    scenario_id: int = Field(foreign_key="interview_scenarios.id")
    text: str
    difficulty: str = "medium"  # "easy" | "medium" | "hard"

    scenario: Optional[InterviewScenario] = Relationship(back_populates="questions")
    attempts: List["Attempt"] = Relationship(back_populates="question")

class InterviewSession(SQLModel, table=True):
    __tablename__ = "interview_sessions"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    scenario_id: int = Field(foreign_key="interview_scenarios.id")
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    status: str = "active"  # "active" | "completed"

    user: Optional[User] = Relationship(back_populates="sessions")
    scenario: Optional[InterviewScenario] = Relationship(back_populates="sessions")
    attempts: List["Attempt"] = Relationship(back_populates="session")

class Attempt(SQLModel, table=True):
    __tablename__ = "attempts"
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="interview_sessions.id")
    user_id: int = Field(foreign_key="users.id")
    question_id: int = Field(foreign_key="questions.id")

    user_answer: str
    ai_feedback: Optional[str] = None       # filled in Step 4
    score: Optional[float] = None           # filled in Step 4
    created_at: datetime = Field(default_factory=datetime.utcnow)

    session: Optional[InterviewSession] = Relationship(back_populates="attempts")
    user: Optional[User] = Relationship(back_populates="attempts")
    question: Optional[Question] = Relationship(back_populates="attempts")
