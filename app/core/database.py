# ==============================================================================
# DATABASE ENGINE & SESSION SETUP (app/core/database.py)
# Description: Initializes SQLAlchemy 2.0 engine, session maker, and 
# declarative base for ORM models.
# ==============================================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Create the SQLAlchemy engine with production-ready connection parameters
# pool_pre_ping=True helps handle dropped database connections gracefully
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

# Create a configured "SessionLocal" class to handle database transactions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for our ORM models to inherit from
Base = declarative_base()

def get_db():
    """
    Dependency function that yields a database session per request,
    ensuring it is safely closed once the request cycle finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()