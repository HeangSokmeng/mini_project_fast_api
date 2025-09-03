# app/routers/users.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..helpers.response_helper import ResponseHelper
from ..middleware.auth.role_middleware import RoleMiddleware
from ..models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/profile")
async def get_profile(current_user: User = Depends(RoleMiddleware.require_staff_or_above)):
    return ResponseHelper.success_response(
        data={
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "role": current_user.role.name,
            "is_active": current_user.is_active
        },
        message="Profile retrieved successfully"
    )


@router.get("/all")
async def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleMiddleware.require_admin_or_above)
):
    users = db.query(User).order_by(User.id.desc()).all()
    users_data = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.name,
            "is_active": user.is_active
        }
        for user in users
    ]
    return ResponseHelper.success_response(
        data=users_data,
        message="Users retrieved successfully"
    )


@router.delete("/delete/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleMiddleware.require_superadmin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return ResponseHelper.error_response(
            message="User not found",
            status_code=404
        )
    db.delete(user)
    db.commit()
    return ResponseHelper.success_response(
        message="User deleted successfully"
    )
