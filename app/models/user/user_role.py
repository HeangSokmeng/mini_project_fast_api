# app/models/user/user_role.py
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from .user import Base


class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # superadmin, admin, staff
    description = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    # Relationship
    users = relationship("User", back_populates="role")
