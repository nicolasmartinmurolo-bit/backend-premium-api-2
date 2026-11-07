# ==============================================================================
# FILE: app/tests/test_items.py
# DESCRIPTION: Comprehensive integration tests for Item management endpoints.
# Validates secure CRUD operations, data isolation between users, and pagination.
# ==============================================================================

from fastapi import status


def test_create_item_success(client):
    """
    Test successful item creation associated with the authenticated user (Happy Path).
    Expected: HTTP 201 Created and correct owner attribution.
    """
    # 1. Register and authenticate user
    client.post(
        "/api/v1/users/",
        json={"email": "itemowner@example.com", "password": "password123", "full_name": "Item Owner"}
    )
    login_res = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "itemowner@example.com", "password": "password123"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create item
    response = client.post(
        "/api/v1/items/",
        headers=headers,
        json={"title": "Test Item", "description": "A very important unit test item."}
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Test Item"
    assert data["description"] == "A very important unit test item."
    assert "id" in data
    assert "owner_id" in data


def test_create_item_unauthorized(client):
    """
    Edge Case: Attempt to create an item without providing a JWT bearer token.
    Expected: HTTP 401 Unauthorized.
    """
    response = client.post(
        "/api/v1/items/",
        json={"title": "Unauthorized Item", "description": "Should fail."}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_items_pagination_and_isolation(client):
    """
    Test paginated item retrieval and strict data isolation between different users.
    Expected: Users can only see their own items, respecting skip/limit query params.
    """
    # ----------------------------------------------------
    # User A Setup & Item Creation
    # ----------------------------------------------------
    client.post("/api/v1/users/", json={"email": "usera@example.com", "password": "password123"})
    token_a = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "usera@example.com", "password": "password123"}
    ).json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Create 3 items for User A
    for i in range(1, 4):
        client.post(
            "/api/v1/items/",
            headers=headers_a,
            json={"title": f"User A Item {i}", "description": f"Description {i}"}
        )

    # ----------------------------------------------------
    # User B Setup & Item Creation
    # ----------------------------------------------------
    client.post("/api/v1/users/", json={"email": "userb@example.com", "password": "password123"})
    token_b = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "userb@example.com", "password": "password123"}
    ).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Create 1 item for User B
    client.post(
        "/api/v1/items/",
        headers=headers_b,
        json={"title": "User B Item 1", "description": "User B exclusive content"}
    )

    # ----------------------------------------------------
    # Assertions: Data Isolation & Pagination
    # ----------------------------------------------------
    # User A should see exactly their 3 items
    res_a = client.get("/api/v1/items/", headers=headers_a)
    assert res_a.status_code == status.HTTP_200_OK
    items_a = res_a.json()
    assert len(items_a) == 3
    assert all("User A" in item["title"] for item in items_a)

    # User B should see exactly their 1 item (strict data isolation check)
    res_b = client.get("/api/v1/items/", headers=headers_b)
    assert res_b.status_code == status.HTTP_200_OK
    items_b = res_b.json()
    assert len(items_b) == 1
    assert items_b[0]["title"] == "User B Item 1"

    # Test Pagination parameters (skip & limit) for User A
    res_paginated = client.get("/api/v1/items/?skip=1&limit=1", headers=headers_a)
    assert res_paginated.status_code == status.HTTP_200_OK
    paginated_data = res_paginated.json()
    assert len(paginated_data) == 1
    assert paginated_data[0]["title"] == "User A Item 2"

def test_read_items_as_superuser(client):
    """
    Test that a superuser can retrieve all items across different users,
    whereas regular users are restricted to their own items.
    Expected: Superuser sees global items; regular user sees only personal items.
    """
    # 1. Create Regular User A and an Item
    client.post("/api/v1/users/", json={"email": "regular_item_user@example.com", "password": "password123"})
    token_regular = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "regular_item_user@example.com", "password": "password123"}
    ).json()["access_token"]
    
    client.post(
        "/api/v1/items/",
        headers={"Authorization": f"Bearer {token_regular}"},
        json={"title": "Regular Item", "description": "Owned by regular user"}
    )

    # 2. Create Superuser and an Item
    client.post("/api/v1/users/", json={
        "email": "superuser_item@example.com",
        "password": "password123",
        "is_superuser": True
    })
    token_superuser = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "superuser_item@example.com", "password": "password123"}
    ).json()["access_token"]
    
    client.post(
        "/api/v1/items/",
        headers={"Authorization": f"Bearer {token_superuser}"},
        json={"title": "Superuser Item", "description": "Owned by admin"}
    )

    # 3. Regular user should only see their own 1 item
    res_regular = client.get("/api/v1/items/", headers={"Authorization": f"Bearer {token_regular}"})
    assert res_regular.status_code == status.HTTP_200_OK
    assert len(res_regular.json()) == 1
    assert res_regular.json()[0]["title"] == "Regular Item"

    # 4. Superuser should see ALL items in the system (2 items total)
    res_super = client.get("/api/v1/items/", headers={"Authorization": f"Bearer {token_superuser}"})
    assert res_super.status_code == status.HTTP_200_OK
    assert len(res_super.json()() if callable(res_super.json()) else res_super.json()) == 2