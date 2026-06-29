import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.models.database import init_db
import os

app = FastAPI(
    title="LifeBridge AI Backend",
    description="Autonomous Healthcare Navigation Agent API for Underserved Communities",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
def startup_event():
    # Initialize SQLite Database tables
    init_db()
    print("SQLite Database initialized successfully.")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "LifeBridge AI",
        "version": "1.0.0",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
