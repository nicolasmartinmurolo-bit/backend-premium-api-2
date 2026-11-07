# ==============================================================================
# APPLICATION CONFIGURATION (app/core/config.py)
# Description: Centralizes application settings and environment variables validation
# using Pydantic v2 Settings. Dynamically assembles the DATABASE_URL to avoid 
# hardcoded ports and enforces 'Fail Fast' validation at startup.
# ==============================================================================

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Settings class utilizing Pydantic BaseSettings to parse environment variables
    from the .env file with strict runtime type checking and dynamic assembly.
    """
    # Application metadata
    PROJECT_NAME: str = "Premium Backend API (v2)"
    API_V1_STR: str = "/api/v1"  # <--- Añadimos esta línea faltante
    
    # Database individual parameters (Decoupled configuration)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # Computed field to dynamically assemble SQLAlchemy connection string safely
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """
        Dynamically constructs the PostgreSQL connection URL using decoupled parameters,
        preventing hardcoded values and supporting parallel local environments.
        """
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Security & JWT configuration
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Pydantic v2 configuration to point to our local .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" # Ignores extra variables present in .env not defined here
    )

# Instantiate settings to be imported across the application
settings = Settings()