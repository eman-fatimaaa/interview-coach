from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Session, select
from typing import Optional
import os

from ..database import get_session
from ..models import User
from ..security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)  # bcrypt safe


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

@router.post("/register", response_model=MeResponse, status_code=201)
def register(req: RegisterRequest, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == req.email)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    role = "admin" if req.email.lower() == os.getenv("ADMIN_EMAIL", "").lower() else "user"

    user = User(
        name=req.name,
        email=req.email,
        password_hash=get_password_hash(req.password),
        role=role,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return MeResponse(id=user.id, name=user.name, email=user.email, role=user.role)

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == req.email)).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.email, "role": user.role})
    return TokenResponse(access_token=token)

# @router.get("/me", response_model=MeResponse)
# def me(user: User = Depends(...)):  # will be patched below to avoid circular import
#     # placeholder to satisfy type checker; real dependency is injected in main.py
#     return user  # pragma: no cover
