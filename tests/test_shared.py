"""Tests for shared file management endpoints."""

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
    monkeypatch.setattr("app.config.SHARED_STORAGE_DIR", test_storage / "shared")

    init_db()
    yield


@pytest.fixture
def client():
    """Provide a test client."""
    with TestClient(app) as test_client:
        yield test_client


class TestUploadSharedFile:
    """Tests for POST /shared/files endpoint."""

    def test_upload_shared_file_success(self, client):
        """Test uploading a shared file returns 201."""
        file_content = b"Hello, World!"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}

        response = client.post("/shared/files", files=files)

        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "File uploaded successfully to shared storage"
        assert data["filename"] == "test.txt"

    def test_upload_shared_file_duplicate(self, client):
        """Test uploading shared file with duplicate name returns 409."""
        file_content = b"Hello, World!"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}

        # Upload first time
        client.post("/shared/files", files=files)

        # Upload second time with same name
        response = client.post("/shared/files", files=files)

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_upload_shared_file_empty(self, client):
        """Test uploading empty shared file."""
        files = {"file": ("empty.txt", io.BytesIO(b""), "text/plain")}

        response = client.post("/shared/files", files=files)

        assert response.status_code == 201


class TestListSharedFiles:
    """Tests for GET /shared/files endpoint."""

    def test_list_shared_files_empty(self, client):
        """Test listing shared files when none exist returns empty list."""
        response = client.get("/shared/files")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_shared_files_multiple(self, client):
        """Test listing multiple shared files."""
        # Upload files
        for i in range(3):
            file_content = f"Content {i}".encode()
            files = {"file": (f"file{i}.txt", io.BytesIO(file_content), "text/plain")}
            client.post("/shared/files", files=files)

        response = client.get("/shared/files")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        filenames = [file["filename"] for file in data]
        assert "file0.txt" in filenames
        assert "file1.txt" in filenames
        assert "file2.txt" in filenames


class TestGetSharedFile:
    """Tests for GET /shared/files/{filename} endpoint."""

    def test_get_shared_file_success(self, client):
        """Test getting shared file info returns 200."""
        file_content = b"Hello, World!"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
        client.post("/shared/files", files=files)

        response = client.get("/shared/files/test.txt")

        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.txt"

    def test_get_shared_file_not_found(self, client):
        """Test getting non-existent shared file returns 404."""
        response = client.get("/shared/files/nonexistent.txt")

        assert response.status_code == 404
        assert "File not found" in response.json()["detail"]


class TestDownloadSharedFile:
    """Tests for GET /shared/files/{filename}/download endpoint."""

    def test_download_shared_file_success(self, client):
        """Test downloading a shared file returns file content."""
        file_content = b"Hello, World!"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
        client.post("/shared/files", files=files)

        response = client.get("/shared/files/test.txt/download")

        assert response.status_code == 200
        assert response.content == file_content
        assert response.headers["content-type"] == "application/octet-stream"

    def test_download_shared_file_not_found(self, client):
        """Test downloading non-existent shared file returns 404."""
        response = client.get("/shared/files/nonexistent.txt/download")

        assert response.status_code == 404
        assert "File not found" in response.json()["detail"]


class TestDeleteSharedFile:
    """Tests for DELETE /shared/files/{filename} endpoint."""

    def test_delete_shared_file_success(self, client):
        """Test deleting an existing shared file returns 200."""
        file_content = b"Hello, World!"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
        client.post("/shared/files", files=files)

        response = client.delete("/shared/files/test.txt")

        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]

        # Verify file is deleted
        get_response = client.get("/shared/files/test.txt")
        assert get_response.status_code == 404

    def test_delete_shared_file_not_found(self, client):
        """Test deleting non-existent shared file returns 404."""
        response = client.delete("/shared/files/nonexistent.txt")

        assert response.status_code == 404
        assert "File not found" in response.json()["detail"]

    def test_delete_shared_file_then_list(self, client):
        """Test that deleted shared file doesn't appear in list."""
        file_content = b"Hello, World!"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
        client.post("/shared/files", files=files)

        client.delete("/shared/files/test.txt")

        list_response = client.get("/shared/files")
        assert list_response.status_code == 200
        filenames = [file["filename"] for file in list_response.json()]
        assert "test.txt" not in filenames
