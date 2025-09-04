from typing import Optional

from pydantic import BaseModel

from app.schemas.category_schema import CategoryOut


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    category_id: int


class ProductOut(ProductBase):
    id: int
    filepath: str
    category: CategoryOut

    class Config:
        orm_mode = True
