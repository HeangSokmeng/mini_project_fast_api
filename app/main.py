
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine
from app.models.user.user import Base
from app.routers import auth, category, products, users

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

# Common prefix
api_prefix = "/api/v1"

# List of routers with optional tags
routers = [
    (auth.router, "Auth"),
    (users.router, "Users"),
    (category.router, "Categories"),
    (products.router, "Products"),
]

# Include all routers under the same prefix
for router, tag in routers:
    app.include_router(router, prefix=api_prefix, tags=[tag])


@app.get("/")
async def root():
    return {"message": "FastAPI Auth System is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running properly"}
