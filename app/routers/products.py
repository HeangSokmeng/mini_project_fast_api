import os

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app import models
from app.core.database import get_db
from app.helpers.response_helper import ResponseHelper

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/products", tags=["Products"])


# ----------------- CREATE -----------------
@router.post("/")
async def create_product(
    name: str = Form(...),
    description: str = Form(None),
    category_id: int = Form(...),
    is_active: bool = Form(True),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        product = models.Product(
            name=name,
            description=description,
            category_id=category_id,
            is_active=is_active,
            filepath=file_path,
        )
        db.add(product)
        db.commit()
        db.refresh(product)

        return ResponseHelper.success_response(
            data={
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "category_id": product.category_id,
                "is_active": product.is_active,
                "filepath": product.filepath
            },
            message="Product created successfully"
        )
    except Exception as e:
        return ResponseHelper.error_response(message=str(e))


# ----------------- READ -----------------
@router.get("/")
def list_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).order_by(models.Product.id.desc()).all()
    products_data = [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "category_id": p.category_id,
            "is_active": p.is_active,
            "filepath": p.filepath
        }
        for p in products
    ]
    return ResponseHelper.success_response(
        data=products_data,
        message="Products retrieved successfully"
    )


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return ResponseHelper.error_response(message="Product not found", status_code=404)

    return ResponseHelper.success_response(
        data={
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "category_id": product.category_id,
            "is_active": product.is_active,
            "filepath": product.filepath
        },
        message="Product retrieved successfully"
    )


# ----------------- UPDATE -----------------
@router.put("/{product_id}")
async def update_product(
    product_id: int,
    name: str = Form(None),
    description: str = Form(None),
    category_id: int = Form(None),
    is_active: bool = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return ResponseHelper.error_response(message="Product not found", status_code=404)

    # Update fields
    if name is not None:
        product.name = name
    if description is not None:
        product.description = description
    if category_id is not None:
        product.category_id = category_id
    if is_active is not None:
        product.is_active = is_active

    # Handle file update
    if file:
        if os.path.exists(product.filepath):
            os.remove(product.filepath)
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        product.filepath = file_path

    db.commit()
    db.refresh(product)

    return ResponseHelper.success_response(
        data={
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "category_id": product.category_id,
            "is_active": product.is_active,
            "filepath": product.filepath
        },
        message="Product updated successfully"
    )


# ----------------- DELETE -----------------
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return ResponseHelper.error_response(message="Product not found", status_code=404)

    if os.path.exists(product.filepath):
        os.remove(product.filepath)

    db.delete(product)
    db.commit()
    return ResponseHelper.success_response(message="Product deleted successfully")
