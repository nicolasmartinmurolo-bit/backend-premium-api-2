# ==============================================================================
# FILE: app/api/deps.py
# DESCRIPTION: Shared API dependencies (Dependency Injection pattern).
# Encapsulates reusable logic such as database session yielding and current 
# authenticated user resolution via JWT tokens.
# ==============================================================================

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db  # <--- Importamos get_db directamente desde database.py
from app.models.user import User as UserModel

# OAuth2 scheme definition pointing to the token generation endpoint.
# This tells FastAPI where clients should send credentials to obtain a token.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> UserModel:
    """
    Validates the incoming JWT bearer token, extracts the subject (user email/id),
    and queries the database to return the active user instance.
    Implements a fail-secure pattern raising 401 Unauthorized if credentials fail.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token using our secret key and algorithm
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Query the user in the database
    user = db.query(UserModel).filter(UserModel.email == user_email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    
    return user