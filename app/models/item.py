# ==============================================================================
# FILE: app/models/item.py
# DESCRIPTION: Item ORM model definition.
# Maps items to the 'items' table and links them to a specific user owner.
# ==============================================================================

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base  # O desde app.models.base si este reexporta correctamente


class Item(Base):
    """
    Database model representing business items owned by users.
    Enforces data isolation through user foreign keys.
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    # Foreign key linking the item to the users table primary key
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Back-populates relationship with the User model
    owner = relationship("User", back_populates="items")