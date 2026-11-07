# ==============================================================================
# FILE: app/api/v1/endpoints/items.py
# DESCRIPTION: Item management endpoints (Protected CRUD with JWT).
# Handles HTTP routes to create and list items linked exclusively to the 
# authenticated user context.
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
    - **item_in**: Pydantic payload containing title and description.
    - **db**: Active database session injection.
    - **current_user**: Validated user model extracted from JWT token.
    """
    # Unpack validated Pydantic model data and inject the owner's foreign key reference
    db_item = ItemModel(**item_in.model_dump(), owner_id=current_user.id)
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)  # Refresh to retrieve database-generated fields (id, timestamps)
    
    return db_item


@router.get("/", response_model=List[Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Retrieve a paginated list of items belonging exclusively to the authenticated user.
    - **skip**: Offset for pagination (default: 0).
    - **limit**: Maximum number of records to return (default: 100).
    """
    items = (
        db.query(ItemModel)
        .filter(ItemModel.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return items