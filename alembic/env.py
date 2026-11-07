# ==============================================================================
# ALEMBIC ENVIRONMENT CONFIGURATION (alembic/env.py)
# Description: Configures Alembic to read database credentials dynamically from 
# our Pydantic settings and registers SQLAlchemy models for 'autogenerate' support.
# ==============================================================================

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 1. Import application settings and declarative Base containing our ORM models
from app.core.config import settings
from app.core.database import Base

# Import all models explicitly so Alembic detects them during autogeneration
from app.models.user import User
from app.models.item import Item

# This is the Alembic Config object, which provides access to values within alembic.ini
config = context.config

# Interpret the config file for Python logging if a config file is present
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. Overwrite SQLAlchemy URL in Alembic config with our dynamic Pydantic settings URL
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# 3. Set target_metadata for 'autogenerate' support (enables Alembic to detect model changes)
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    Outputs SQL statements directly to stdout without executing them on a live engine.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    Creates an Engine and associates a connection with the transaction context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()