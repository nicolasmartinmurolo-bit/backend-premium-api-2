# ==============================================================================
# FILE: app/schemas/item.py
# DESCRIPTION: Pydantic schemas for Item validation and serialization.
# Handles incoming data validation (creation/updates) and database model output formatting.
# ==============================================================================

from typing import Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    """Shared base properties for items."""
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    """Properties required to create a new item."""
    pass


class ItemUpdate(ItemBase):
    """Properties that can be modified during an item update (all optional)."""
    title: Optional[str] = None


class Item(ItemBase):
    """
    Properties returned to the client via public API endpoints.
    Includes database-generated IDs and the foreign key reference to the owner.
    """
    id: int
    owner_id: int

    # Config to allow Pydantic to read data directly from SQLAlchemy ORM models
    model_config = {"from_attributes": True}