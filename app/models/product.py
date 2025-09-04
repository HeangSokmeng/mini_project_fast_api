# app/models/product.py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    filepath = Column(String(255), nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="products")
