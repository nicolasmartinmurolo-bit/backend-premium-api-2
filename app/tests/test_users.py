# ==============================================================================
# FILE: app/tests/test_users.py
# DESCRIPTION: Comprehensive integration tests for users, authentication, and edge cases.
# ==============================================================================

from fastapi import status
from jose import jwt
from app.core.config import settings


def test_read_root(client):
    """Test application liveness root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_user_success(client):
    """Test successful user registration (Happy Path)."""
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "password": "securepassword123",
            "full_name": "Test User",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data  # Security check: Password must never be leaked


def test_create_user_duplicate_email(client):
    """
    Edge Case: Attempt to register a user with an already existing email.
    Expected: HTTP 400 Bad Request.
    """
    payload = {
        "email": "duplicate@example.com",
        "password": "password123",
    }
    # First registration (Success)
    response_1 = client.post("/api/v1/users/", json=payload)
    assert response_1.status_code == status.HTTP_201_CREATED

    # Second registration with same email (Edge Case Failure)
    response_2 = client.post("/api/v1/users/", json=payload)
    assert response_2.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response_2.json()["detail"]


def test_login_success(client):
    """Test successful OAuth2 login and JWT access token retrieval."""
    # Register user first
    client.post(
        "/api/v1/users/",
        json={"email": "login@example.com", "password": "mypassword"},
    )

    # Attempt login via OAuth2 form data structure
    response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "login@example.com", "password": "mypassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_incorrect_credentials(client):
    """
    Edge Case: Login attempt with invalid password or non-existent email.
    Expected: HTTP 400 Bad Request.
    """
    response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "notfound@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Incorrect" in response.json()["detail"]


def test_login_inactive_user(client):
    """
    Edge Case: Attempt to login with a valid user whose account is inactive (is_active=False).
    Expected: HTTP 400 Bad Request ("Inactive user account").
    """
    client.post(
        "/api/v1/users/",
        json={
            "email": "inactive@example.com",
            "password": "password123",
            "is_active": False,
        },
    )

    response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "inactive@example.com", "password": "password123"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Inactive user account" in response.json()["detail"]


def test_access_protected_route_unauthorized(client):
    """
    Edge Case: Accessing a protected endpoint (/api/v1/users/me) without a token.
    Expected: HTTP 401 Unauthorized.
    """
    response = client.get("/api/v1/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_access_protected_route_invalid_token(client):
    """
    Edge Case: Accessing a protected route with a malformed or invalid token.
    Expected: HTTP 401 Unauthorized.
    """
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid_token_string_123"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_access_protected_route_token_missing_sub(client):
    """
    Edge Case: Accessing a protected route with a validly signed token 
    that lacks the 'sub' (subject) claim.
    Expected: HTTP 401 Unauthorized.
    """
    bad_payload = {"exp": 9999999999}
    bad_token = jwt.encode(bad_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {bad_token}"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_access_protected_route_user_not_found(client):
    """
    Edge Case: Token contains a valid email format ('sub'), but the user 
    does not actually exist in the database anymore.
    Expected: HTTP 404 Not Found.
    """
    ghost_payload = {"sub": "ghost@example.com"}
    ghost_token = jwt.encode(ghost_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {ghost_token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "User not found" in response.json()["detail"]


def test_superuser_permissions_forbidden(client):
    """
    Edge Case: Standard user attempting to access admin-only endpoint (GET /users/).
    Expected: HTTP 403 Forbidden.
    """
    client.post(
        "/api/v1/users/",
        json={"email": "regular@example.com", "password": "password123"},
    )
    login_res = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "regular@example.com", "password": "password123"},
    )
    token = login_res.json()["access_token"]

    response = client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "privileges" in response.json()["detail"]