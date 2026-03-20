"""Tests for file management endpoints."""

import io

import pytest
from fastapi.testclient import TestClient

from app.database import init_db
from app.main import app


@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    """Set up a test database and storage for each test."""
    test_db = tmp_path / "test_database.db"
    test_storage = tmp_path / "storage"
    test_storage.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr("app.database.DATABASE_PATH", test_db)
    monkeypatch.setattr("app.config.USERS_STORAGE_DIR", test_storage / "users")

    init_db()
    yield


@pytest.fixture
def client():
    """Provide a test client."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_user(client):
    """Create a test user and return user info."""
    response = client.post("/users", json={"username": "testuser"})
    return response.json()


class TestUploadFile:
    """Tests for POST /users/{user_id}/files endpoint."""

    def test_upload_file_success(self, client, test_user):
        """Test uploading a file returns 201."""
        file_content = b"Hello, World!"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}

        response = client.post(
            f"/users/{test_user['id']}/files",
            files=files,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "File uploaded successfully"
        assert data["filename"] == "test.txt"
        assert data["user_id"] == test_user["id"]

    def test_upload_file_user_not_found(self, client):
        """Test uploading file for non-existent user returns 404."""
        file_content = b"Hello, World!"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}

        response = client.post("/users/999/files", files=files)

        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    def test_upload_file_duplicate(self, client, test_user):
        """Test uploading file with duplicate name returns 409."""
        file_content = b"Hello, World!"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}

        # Upload first time
        client.post(f"/users/{test_user['id']}/files", files=files)

        # Upload second time with same name
        response = client.post(
            f"/users/{test_user['id']}/files",
            files=files,
        )

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_upload_file_empty(self, client, test_user):
        """Test uploading empty file."""
        files = {"file": ("empty.txt", io.BytesIO(b""), "text/plain")}

        response = client.post(
            f"/users/{test_user['id']}/files",
            files=files,
        )

        assert response.status_code == 201


class TestListFiles:
    """Tests for GET /users/{user_id}/files endpoint."""

    def test_list_files_empty(self, client, test_user):
        """Test listing files when user has no files returns empty list."""
        response = client.get(f"/users/{test_user['id']}/files")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_files_multiple(self, client, test_user):
        """Test listing multiple files."""
        # Upload files
        for i in range(3):
            file_content = f"Content {i}".encode()
            files = {"file": (f"file{i}.txt", io.BytesIO(file_content), "text/plain")}
            client.post(f"/users/{test_user['id']}/files", files=files)

        response = client.get(f"/users/{test_user['id']}/files")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        filenames = [file["filename"] for file in data]
        assert "file0.txt" in filenames
        assert "file1.txt" in filenames
        assert "file2.txt" in filenames

    def test_list_files_user_not_found(self, client):
        """Test listing files for non-existent user returns 404."""
        response = client.get("/users/999/files")

        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]


class TestGetFile:
    """Tests for GET /users/{user_id}/files/{filename} endpoint."""

    def test_get_file_success(self, client, test_user):
        """Test getting file info returns 200."""
        file_content = b"Hello, World!"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
        client.post(f"/users/{test_user['id']}/files", files=files)

        response = client.get(f"/users/{test_user['id']}/files/test.txt")

        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.txt"
        assert data["user_id"] == test_user["id"]

    def test_get_file_not_found(self, client, test_user):
        """Test getting non-existent file returns 404."""
        response = client.get(f"/users/{test_user['id']}/files/nonexistent.txt")

        assert response.status_code == 404
        assert "File not found" in response.json()["detail"]

    def test_get_file_user_not_found(self, client):
        """Test getting file for non-existent user returns 404."""
        response = client.get("/users/999/files/test.txt")

        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]


class TestDownloadFile:
    """Tests for GET /users/{user_id}/files/{filename}/download endpoint."""

    def test_download_file_success(self, client, test_user):
        """Test downloading a file returns file content."""
        file_content = b"Hello, World!"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
        client.post(f"/users/{test_user['id']}/files", files=files)

        response = client.get(f"/users/{test_user['id']}/files/test.txt/download")

        assert response.status_code == 200
        assert response.content == file_content
        assert response.headers["content-type"] == "application/octet-stream"

    def test_download_file_not_found(self, client, test_user):
        """Test downloading non-existent file returns 404."""
        response = client.get(
            f"/users/{test_user['id']}/files/nonexistent.txt/download"
        )

        assert response.status_code == 404
        assert "File not found" in response.json()["detail"]

    def test_download_file_user_not_found(self, client):
        """Test downloading file for non-existent user returns 404."""
        response = client.get("/users/999/files/test.txt/download")

        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]


class TestDeleteFile:
    """Tests for DELETE /users/{user_id}/files/{filename} endpoint."""

    def test_delete_file_success(self, client, test_user):
        """Test deleting an existing file returns 200."""
        file_content = b"Hello, World!"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
        client.post(f"/users/{test_user['id']}/files", files=files)

        response = client.delete(f"/users/{test_user['id']}/files/test.txt")

        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]

        # Verify file is deleted
        get_response = client.get(f"/users/{test_user['id']}/files/test.txt")
        assert get_response.status_code == 404

    def test_delete_file_not_found(self, client, test_user):
        """Test deleting non-existent file returns 404."""
        response = client.delete(f"/users/{test_user['id']}/files/nonexistent.txt")

        assert response.status_code == 404
        assert "File not found" in response.json()["detail"]

    def test_delete_file_user_not_found(self, client):
        """Test deleting file for non-existent user returns 404."""
        response = client.delete("/users/999/files/test.txt")

        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    def test_delete_file_then_list(self, client, test_user):
        """Test that deleted file doesn't appear in list."""
        file_content = b"Hello, World!"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
        client.post(f"/users/{test_user['id']}/files", files=files)

        client.delete(f"/users/{test_user['id']}/files/test.txt")

        list_response = client.get(f"/users/{test_user['id']}/files")
        assert list_response.status_code == 200
        filenames = [file["filename"] for file in list_response.json()]
        assert "test.txt" not in filenames


class TestFileIsolation:
    """Tests for file isolation between users."""

    def test_files_isolated_between_users(self, client):
        """Test that files are isolated between users."""
        # Create two users
        user1 = client.post("/users", json={"username": "user1"}).json()
        user2 = client.post("/users", json={"username": "user2"}).json()

        # Upload file to user1
        file_content = b"User1 file"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
        client.post(f"/users/{user1['id']}/files", files=files)

        # User2 should have empty file list
        response = client.get(f"/users/{user2['id']}/files")
        assert response.status_code == 200
        assert len(response.json()) == 0

        # User2 cannot access user1's file
        response = client.get(f"/users/{user2['id']}/files/test.txt")
        assert response.status_code == 404

    def test_same_filename_different_users(self, client):
        """Test that same filename works for different users."""
        # Create two users
        user1 = client.post("/users", json={"username": "user1"}).json()
        user2 = client.post("/users", json={"username": "user2"}).json()

        # Upload same filename to both users
        files1 = {"file": ("test.txt", io.BytesIO(b"User1"), "text/plain")}
        files2 = {"file": ("test.txt", io.BytesIO(b"User2"), "text/plain")}

        client.post(f"/users/{user1['id']}/files", files=files1)
        client.post(f"/users/{user2['id']}/files", files=files2)

        # Both should have one file
        list1 = client.get(f"/users/{user1['id']}/files").json()
        list2 = client.get(f"/users/{user2['id']}/files").json()
        assert len(list1) == 1
        assert len(list2) == 1

        # Download should return different content
        download1 = client.get(f"/users/{user1['id']}/files/test.txt/download")
        download2 = client.get(f"/users/{user2['id']}/files/test.txt/download")
        assert download1.content == b"User1"
        assert download2.content == b"User2"
