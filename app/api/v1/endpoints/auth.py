# ==============================================================================
# FILE: app/api/v1/endpoints/auth.py
# DESCRIPTION: Authentication and Login endpoints (OAuth2 implementation).
# Handles identity verification and JWT access token generation.
# ==============================================================================

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.user import User as UserModel
from app.schemas.token import Token

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login endpoint. Verifies user credentials and returns a JWT bearer token.
    - **form_data.username**: Expected to be the user's email address.
    - **form_data.password**: Plain text password to verify against hashed database record.
    """
    # 1. Query user by email (username field in OAuth2 spec)
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    
    # 2. Validate user existence and password correctness
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    
    # 3. Check if user account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account",
        )
    
    # 4. Generate expiration delta and sign JWT access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }