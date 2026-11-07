# ==============================================================================
# FILE: app/models/base.py
# DESCRIPTION: SQLAlchemy declarative base configuration.
# Acts as the central registry for all ORM models to support database migrations.
# ==============================================================================

# Declarative base class from which all database models will inherit.
from app.core.database import Base