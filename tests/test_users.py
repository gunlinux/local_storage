"""Tests for user management endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.database import init_db
from app.main import app


@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    """Set up a test database for each test."""
    test_db = tmp_path / "test_database.db"
    monkeypatch.setattr("app.database.DATABASE_PATH", test_db)
    init_db()
    yield


@pytest.fixture
def client():
    """Provide a test client."""
    with TestClient(app) as test_client:
        yield test_client


class TestCreateUser:
    """Tests for POST /users endpoint."""

    def test_create_user_success(self, client):
        """Test creating a new user returns 201."""
        response = client.post("/users", json={"username": "testuser"})

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser"
        assert "id" in data
        assert "created_at" in data

    def test_create_user_duplicate_username(self, client):
        """Test creating user with duplicate username returns 400."""
        client.post("/users", json={"username": "testuser"})
        response = client.post("/users", json={"username": "testuser"})

        assert response.status_code == 400
        assert "Username already exists" in response.json()["detail"]

    def test_create_user_empty_username(self, client):
        """Test creating user with empty username returns 422."""
        response = client.post("/users", json={"username": ""})

        assert response.status_code == 422

    def test_create_user_long_username(self, client):
        """Test creating user with username > 50 chars returns 422."""
        response = client.post("/users", json={"username": "a" * 51})

        assert response.status_code == 422


class TestListUsers:
    """Tests for GET /users endpoint."""

    def test_list_users_empty(self, client):
        """Test listing users when no users exist returns empty list."""
        response = client.get("/users")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_users_multiple(self, client):
        """Test listing multiple users."""
        client.post("/users", json={"username": "user1"})
        client.post("/users", json={"username": "user2"})
        client.post("/users", json={"username": "user3"})

        response = client.get("/users")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        usernames = [user["username"] for user in data]
        assert "user1" in usernames
        assert "user2" in usernames
        assert "user3" in usernames


class TestGetUser:
    """Tests for GET /users/{user_id} endpoint."""

    def test_get_user_success(self, client):
        """Test getting an existing user returns 200."""
        create_response = client.post("/users", json={"username": "testuser"})
        user_id = create_response.json()["id"]

        response = client.get(f"/users/{user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == "testuser"

    def test_get_user_not_found(self, client):
        """Test getting non-existent user returns 404."""
        response = client.get("/users/999")

        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]


class TestDeleteUser:
    """Tests for DELETE /users/{user_id} endpoint."""

    def test_delete_user_success(self, client):
        """Test deleting an existing user returns 200."""
        create_response = client.post("/users", json={"username": "testuser"})
        user_id = create_response.json()["id"]

        response = client.delete(f"/users/{user_id}")

        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]

        # Verify user is deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404

    def test_delete_user_not_found(self, client):
        """Test deleting non-existent user returns 404."""
        response = client.delete("/users/999")

        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    def test_delete_user_then_list(self, client):
        """Test that deleted user doesn't appear in list."""
        create_response = client.post("/users", json={"username": "testuser"})
        user_id = create_response.json()["id"]

        client.delete(f"/users/{user_id}")

        list_response = client.get("/users")
        assert list_response.status_code == 200
        user_ids = [user["id"] for user in list_response.json()]
        assert user_id not in user_ids
