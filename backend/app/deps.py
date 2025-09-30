from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from .database import get_session
from .models import User
from .security import decode_token  

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = session.exec(select(User).where(User.id == payload.get("sub"))).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    return user

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

 
    user_id = payload.get("sub")
    email = payload.get("email")

    user = None
    if user_id:
        user = session.get(User, user_id)
    elif email:
        user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

