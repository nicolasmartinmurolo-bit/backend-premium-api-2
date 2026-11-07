# ==============================================================================
# FILE: app/api/v1/endpoints/items.py
# DESCRIPTION: Item management endpoints (Protected CRUD with JWT & RBAC).
# Handles HTTP routes to create and list items with superuser privilege extensions.
# ==============================================================================

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.item import Item as ItemModel
from app.models.user import User as UserModel
from app.schemas.item import Item, ItemCreate

router = APIRouter()


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(
    item_in: ItemCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Create a new item associated automatically with the currently authenticated user.
    """
    db_item = ItemModel(**item_in.model_dump(), owner_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/", response_model=List[Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Retrieve a paginated list of items.
    - If user is a superuser: Returns ALL items in the database.
    - If user is a regular user: Returns ONLY items belonging to the authenticated user.
    """
    if current_user.is_superuser:
        # Superuser role bypasses tenant isolation to inspect all system items
        items = db.query(ItemModel).offset(skip).limit(limit).all()
    else:
        # Regular user strict data isolation
        items = (
            db.query(ItemModel)
            .filter(ItemModel.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    return items