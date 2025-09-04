# app/models/category.py
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)

    products = relationship("Product", back_populates="category")
