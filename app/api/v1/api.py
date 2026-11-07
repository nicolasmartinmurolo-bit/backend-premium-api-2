# ==============================================================================
# FILE: app/api/v1/api.py
# DESCRIPTION: API Version 1 central router aggregator.
# Combines individual routers (auth, users, items) into a single API router
# to be mounted cleanly in the main FastAPI application.
# ==============================================================================

from fastapi import APIRouter
from app.api.v1.endpoints import items, users, auth  # (auth se añadirá próximamente)

api_router = APIRouter()

# Register sub-routers with specific prefixes and tags for OpenAPI documentation
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])