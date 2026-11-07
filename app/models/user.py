# ==============================================================================
# FILE: app/models/user.py
# DESCRIPTION: User ORM model definition.
# Maps the Python class to the 'users' table in PostgreSQL.
# ==============================================================================

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base  # O desde app.models.base si este reexporta correctamente


class User(Base):
    """
    Database model representing system users.
    Handles user credentials, status flags, and relationships with business items.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Relationship mapping: One user can own multiple items.
    # cascade="all, delete-orphan" ensures items are cleaned up if the user is deleted.
    # items = relationship("Item", back_owner="owner", cascade="all, delete-orphan")
    # Note: In modern SQLAlchemy 2.0+, relationships typically use `back_populates` instead of `back_owner`.
    items = relationship("Item", back_populates="owner", cascade="all, delete-orphan")