from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .config import APP_NAME
from .routers import health, ai, auth
from .database import init_db
from .deps import get_current_user
from .models import User

app = FastAPI(title=APP_NAME)

# CORS: in dev allow all; we’ll lock down later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
@app.on_event("startup")
def on_startup():
    init_db()

# Inject the real dependency for /auth/me (to avoid circular import)
@auth.router.get("/me", response_model=dict)
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}

# Routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"message": "AI Interview Coach API is running"}
