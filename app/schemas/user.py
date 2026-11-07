# ==============================================================================
# FILE: app/schemas/user.py
# DESCRIPTION: Pydantic schemas for User validation (Create, Update, Read).
# ==============================================================================

from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Shared properties for user schemas."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserCreate(UserBase):
    """Properties required during user registration (Plain password received)."""
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    """Properties that can be modified during a user update."""
    password: Optional[str] = None


class UserInDBBase(UserBase):
    """
    Base schema for users stored in database (includes internal IDs).
    'from_attributes = True' (formerly known as 'orm_mode' in Pydantic V1) 
    allows Pydantic to read data directly from SQLAlchemy ORM model instances 
    instead of requiring flat dictionaries, enabling seamless serialization 
    from database objects to JSON responses.
    """
    id: Optional[int] = None

    model_config = {"from_attributes": True}


class User(UserInDBBase):
    """Properties to return via public API endpoints (Password excluded!)."""
    pass