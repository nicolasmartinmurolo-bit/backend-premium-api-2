# ==============================================================================
# FILE: app/api/v1/endpoints/users.py
# DESCRIPTION: User management endpoints (Registration, Profile, and Admin listing).
# ==============================================================================

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate

router = APIRouter()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user in the system. Enforces uniqueness check on email.
    - **user_in**: Pydantic schema containing email, plain password, and metadata.
    """
    # 1. Check if user already exists (Edge case: Duplicate email)
    existing_user = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    
    # 2. Hash password securely using our direct bcrypt implementation
    hashed_password = get_password_hash(user_in.password)
    
    # 3. Create ORM model instance
    db_user = UserModel(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.get("/me", response_model=User)
def read_user_me(current_user: UserModel = Depends(get_current_user)):
    """
    Retrieve the profile of the currently authenticated user via JWT bearer token.
    """
    return current_user


@router.get("/", response_model=List[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Retrieve all users. Restricted exclusively to superusers (Role-based access guard).
    """
    # Edge case: Authorization guard (Forbidden if not superuser)
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users