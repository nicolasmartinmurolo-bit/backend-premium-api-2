"""
================================================================================
MODULE: Security, Hashing, and JWT Authentication (app/core/security.py)
================================================================================
Description:
    This module centralizes all cryptographic logic for the application:
    1. Unidirectional password hashing using the 'bcrypt' library directly 
       (mitigating compatibility issues found in legacy wrappers).
    2. Generation, signing, and decoding of JSON Web Tokens (JWT) to enforce 
       a stateless authentication architecture.
================================================================================
"""

from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import jwt
import bcrypt

from app.core.config import settings

# ==============================================================================
# PASSWORD HASHING FUNCTIONS
# ==============================================================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a securely hashed counterpart.
    
    Args:
        plain_password (str): The raw password provided by the user during login.
        hashed_password (str): The secure hash stored in the database.
        
    Returns:
        bool: True if passwords match, False otherwise.
    """
    # bcrypt requires bytes; encode strings accordingly
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)


def get_password_hash(password: str) -> str:
    """
    Generate a secure cryptographic hash from a plain text password using bcrypt.
    
    Security Note: 
    Bcrypt has a native hard limit of 72 bytes maximum. To prevent system errors 
    or unpredictable behavior with excessively long passwords, we encode the string 
    to bytes and apply a preventive truncation at the first 72 bytes.
    
    Args:
        password (str): The raw password to be encrypted.
        
    Returns:
        str: The resulting secure hash string ready to be stored in the database.
    """
    pwd_bytes = password.encode('utf-8')
    if len(pwd_bytes) > 72:
        pwd_bytes = pwd_bytes[:72]
        
    # Generate a random salt and hash the password using bcrypt directly
    hashed_password = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
    
    return hashed_password.decode('utf-8')


# ==============================================================================
# JSON WEB TOKEN (JWT) FUNCTIONS
# ==============================================================================

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a signed JSON Web Token (JWT) for stateless user authorization.
    
    Args:
        subject (Union[str, Any]): The unique identifier for the token payload (typically user email/id).
        expires_delta (Optional[timedelta]): Custom expiration time window. Defaults to system settings.
        
    Returns:
        str: Encoded JWT access token string.
    """
    # Handle token expiration calculation with fallback logic:
    if expires_delta:
        # Custom expiration scenario: Executed when an explicit argument is passed.
        # Use Case: Useful for features like "Remember Me" (e.g., 7 days expiration) 
        # or short-lived tokens like password reset tokens (e.g., 15 minutes).
        expire = datetime.utcnow() + expires_delta
    else:
        # Default expiration scenario: Executed when no custom delta is specified.
        # Fallbacks automatically to the standard configuration defined in settings 
        # (settings.ACCESS_TOKEN_EXPIRE_MINUTES, typically 30 minutes for standard logins).
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    # Construct the payload dictionary
    to_encode = {"exp": expire, "sub": str(subject)}
    
    # Encode and sign the JWT using the secret key and algorithm defined in settings
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt