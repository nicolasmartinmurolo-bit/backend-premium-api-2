# ==============================================================================
# FILE: app/schemas/token.py
# DESCRIPTION: Pydantic schemas for token and authentication payload validation.
# ==============================================================================

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Schema representing the JWT access token response structure."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema representing the payload data encoded inside the JWT token."""
    email: Optional[str] = None