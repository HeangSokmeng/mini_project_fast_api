# app/middleware/auth/role_middleware.py
from typing import List

from fastapi import Depends, HTTPException, status

from ...models import User
from .auth_middleware import AuthMiddleware


class RoleMiddleware:
    @staticmethod
    def require_roles(allowed_roles: List[str]):
        def role_checker(current_user: User = Depends(AuthMiddleware.get_current_user)):
            if current_user.role.name not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
                )
            return current_user
        return role_checker

    @staticmethod
    def require_superadmin(current_user: User = Depends(AuthMiddleware.get_current_user)):
        if current_user.role.name != "superadmin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Superadmin role required."
            )
        return current_user

    @staticmethod
    def require_admin_or_above(current_user: User = Depends(AuthMiddleware.get_current_user)):
        allowed_roles = ["superadmin", "admin"]
        if current_user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Admin or Superadmin role required."
            )
        return current_user

    @staticmethod
    def require_staff_or_above(current_user: User = Depends(AuthMiddleware.get_current_user)):
        allowed_roles = ["superadmin", "admin", "staff"]
        if current_user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Staff role or above required."
            )
        return current_user
