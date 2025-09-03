# app/routers/auth.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..core.config import settings
from ..core.database import get_db
from ..helpers.response_helper import ResponseHelper
from ..helpers.token_helper import TokenHelper
from ..middleware.auth.role_middleware import RoleMiddleware
from ..models import User, UserRole
from ..schemas.auth.login_schema import LoginRequest
from ..schemas.auth.register_schema import RegisterRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])
token_helper = TokenHelper(secret_key=settings.SECRET_KEY)


@router.post("/login")
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not user.verify_password(login_data.password):
        return ResponseHelper.error_response(
            message="Invalid email or password",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    if not user.is_active:
        return ResponseHelper.error_response(
            message="Account is inactive",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    # Create access token
    access_token = token_helper.create_access_token(
        data={"sub": str(user.id), "role": user.role.name}
    )
    return ResponseHelper.success_response(
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.name
            }
        },
        message="Login successful"
    )


@router.post("/register")
async def register(register_data: RegisterRequest, db: Session = Depends(get_db), current_user: User = Depends(RoleMiddleware.require_superadmin)):
    # Check if user exists
    if db.query(User).filter(User.email == register_data.email).first():
        return ResponseHelper.error_response(
            message="Email already registered",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    if db.query(User).filter(User.username == register_data.username).first():
        return ResponseHelper.error_response(
            message="Username already taken",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    # Get role
    role = db.query(UserRole).filter(UserRole.name == register_data.role_name).first()
    if not role:
        return ResponseHelper.error_response(
            message="Invalid role specified",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    # Create user
    hashed_password = User.get_password_hash(register_data.password)
    new_user = User(
        username=register_data.username,
        email=register_data.email,
        hashed_password=hashed_password,
        full_name=register_data.full_name,
        role_id=role.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return ResponseHelper.success_response(
        data={
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "role": role.name
        },
        message="User registered successfully",
        status_code=status.HTTP_201_CREATED
    )
