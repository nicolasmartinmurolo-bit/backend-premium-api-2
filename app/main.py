# ==============================================================================
# FILE: app/main.py
# DESCRIPTION: Main FastAPI Application Entrypoint.
# Initializes the FastAPI app instance, registers global middlewares, 
# and mounts the API v1 router.
# ==============================================================================

from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings

# Initialize FastAPI app with metadata from configuration
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Production-grade RESTful API built with FastAPI and PostgreSQL."
)

# Mount the main API router under the v1 prefix
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Root"])
def read_root():
    """Root health-check endpoint to verify API liveness."""
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "message": "Welcome to the Premium Backend API v1 stable core."
    }