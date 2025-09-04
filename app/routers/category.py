# app/routers/categories.py
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.helpers.response_helper import ResponseHelper
from app.models.category import Category
from app.schemas.category_schema import CategoryCreate

router = APIRouter(prefix="/categories", tags=["Categories"])


# ----------------- CREATE -----------------
@router.post("/")
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    # Check if category exists
    existing = db.query(Category).filter(Category.name == category_data.name).first()
    if existing:
        return ResponseHelper.error_response(
            message="Category already exists", status_code=400
        )

    # Create new category
    category = Category(
        name=category_data.name,
        description=category_data.description,
        is_active=category_data.is_active
    )
    db.add(category)
    db.commit()
    db.refresh(category)

    return ResponseHelper.success_response(
        data={
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "is_active": category.is_active
        },
        message="Category created successfully"
    )


# ----------------- READ -----------------
@router.get("/")
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).order_by(Category.id.desc()).all()
    categories_data = [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "is_active": c.is_active
        }
        for c in categories
    ]
    return ResponseHelper.success_response(
        data=categories_data,
        message="Categories retrieved successfully"
    )


@router.get("/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return ResponseHelper.error_response(message="Category not found", status_code=404)
    return ResponseHelper.success_response(
        data={
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "is_active": category.is_active
        },
        message="Category retrieved successfully"
    )


# ----------------- UPDATE -----------------
@router.put("/{category_id}")
def update_category(
    category_id: int,
    name: str = Form(None),
    description: str = Form(None),
    is_active: bool = Form(None),
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return ResponseHelper.error_response(message="Category not found", status_code=404)

    if name is not None:
        category.name = name
    if description is not None:
        category.description = description
    if is_active is not None:
        category.is_active = is_active

    db.commit()
    db.refresh(category)
    return ResponseHelper.success_response(
        data={
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "is_active": category.is_active
        },
        message="Category updated successfully"
    )


# ----------------- DELETE -----------------
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return ResponseHelper.error_response(message="Category not found", status_code=404)

    db.delete(category)
    db.commit()
    return ResponseHelper.success_response(message="Category deleted successfully")
