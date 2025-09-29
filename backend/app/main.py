from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .config import APP_NAME
from .routers import health, ai, auth, scenarios, interview
from .database import init_db
from .deps import get_current_user
from .models import User

app = FastAPI(title=APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock down later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

# Bind /auth/me here (avoid circulars)
@auth.router.get("/me", response_model=dict)
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(scenarios.router)
app.include_router(interview.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"message": "AI Interview Coach API is running"}
