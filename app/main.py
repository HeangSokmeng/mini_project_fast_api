
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine
from app.models.user.user import Base
from app.routers import auth, users

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Auth System",
    description="Professional FastAPI authentication system with role-based access control",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "FastAPI Auth System is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running properly"}
