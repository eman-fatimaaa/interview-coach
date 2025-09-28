
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import APP_NAME
from .routers import health, ai

app = FastAPI(title=APP_NAME)

# CORS - allow frontend dev server (vite) and localhost (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In later steps we'll restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"message": "AI Interview Coach API is running"}
