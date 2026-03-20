"""Tests for file upload/download integrity."""

import hashlib
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


@pytest.fixture
def test_user(client):
    """Create a test user."""
    response = client.post("/users", json={"username": "testuser"})
    return response.json()


class TestFileIntegrity:
    """Tests for file upload/download integrity."""

    def test_user_file_integrity_small(self, client, test_user):
        """Test small file integrity - uploaded content matches downloaded."""
        file_content = b"Hello, World!"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}

        # Upload
        upload_response = client.post(
            f"/users/{test_user['id']}/files", files=files
        )
        assert upload_response.status_code == 201

        # Download
        download_response = client.get(
            f"/users/{test_user['id']}/files/test.txt/download"
        )
        assert download_response.status_code == 200
        assert download_response.content == file_content

    def test_user_file_integrity_large(self, client, test_user):
        """Test large file integrity (1MB)."""
        file_content = b"x" * (1024 * 1024)  # 1MB
        files = {"file": ("large.bin", io.BytesIO(file_content), "application/octet-stream")}

        # Upload
        upload_response = client.post(
            f"/users/{test_user['id']}/files", files=files
        )
        assert upload_response.status_code == 201

        # Download
        download_response = client.get(
            f"/users/{test_user['id']}/files/large.bin/download"
        )
        assert download_response.status_code == 200
        assert download_response.content == file_content
        assert len(download_response.content) == 1024 * 1024

    def test_user_file_integrity_binary(self, client, test_user):
        """Test binary file integrity (simulated image)."""
        # Binary content with null bytes
        file_content = b"\x89PNG\r\n\x1a\n" + b"\x00" * 1000
        files = {"file": ("image.png", io.BytesIO(file_content), "image/png")}

        # Upload
        upload_response = client.post(
            f"/users/{test_user['id']}/files", files=files
        )
        assert upload_response.status_code == 201

        # Download
        download_response = client.get(
            f"/users/{test_user['id']}/files/image.png/download"
        )
        assert download_response.status_code == 200
        assert download_response.content == file_content

    def test_user_file_integrity_hash(self, client, test_user):
        """Test file integrity using MD5 hash."""
        file_content = b"Test content for hash verification" * 100
        files = {"file": ("hash_test.txt", io.BytesIO(file_content), "text/plain")}

        # Calculate original hash
        original_hash = hashlib.md5(file_content).hexdigest()

        # Upload
        upload_response = client.post(
            f"/users/{test_user['id']}/files", files=files
        )
        assert upload_response.status_code == 201

        # Download
        download_response = client.get(
            f"/users/{test_user['id']}/files/hash_test.txt/download"
        )
        assert download_response.status_code == 200

        # Calculate downloaded hash
        downloaded_hash = hashlib.md5(download_response.content).hexdigest()

        assert original_hash == downloaded_hash

    def test_shared_file_integrity_small(self, client):
        """Test small shared file integrity."""
        file_content = b"Shared file content"
        files = {"file": ("shared.txt", io.BytesIO(file_content), "text/plain")}

        # Upload
        upload_response = client.post("/shared/files", files=files)
        assert upload_response.status_code == 201

        # Download
        download_response = client.get("/shared/files/shared.txt/download")
        assert download_response.status_code == 200
        assert download_response.content == file_content

    def test_shared_file_integrity_large(self, client):
        """Test large shared file integrity (1MB)."""
        file_content = b"y" * (1024 * 1024)  # 1MB
        files = {"file": ("large_shared.bin", io.BytesIO(file_content), "application/octet-stream")}

        # Upload
        upload_response = client.post("/shared/files", files=files)
        assert upload_response.status_code == 201

        # Download
        download_response = client.get("/shared/files/large_shared.bin/download")
        assert download_response.status_code == 200
        assert download_response.content == file_content
        assert len(download_response.content) == 1024 * 1024

    def test_shared_file_integrity_hash(self, client):
        """Test shared file integrity using MD5 hash."""
        file_content = b"Shared test content for hash verification" * 100
        files = {"file": ("hash_test_shared.txt", io.BytesIO(file_content), "text/plain")}

        # Calculate original hash
        original_hash = hashlib.md5(file_content).hexdigest()

        # Upload
        upload_response = client.post("/shared/files", files=files)
        assert upload_response.status_code == 201

        # Download
        download_response = client.get("/shared/files/hash_test_shared.txt/download")
        assert download_response.status_code == 200

        # Calculate downloaded hash
        downloaded_hash = hashlib.md5(download_response.content).hexdigest()

        assert original_hash == downloaded_hash

    def test_multiple_files_integrity(self, client, test_user):
        """Test integrity of multiple files uploaded sequentially."""
        files_data = [
            ("file1.txt", b"Content 1"),
            ("file2.txt", b"Content 2"),
            ("file3.txt", b"Content 3"),
        ]

        # Upload multiple files
        for filename, content in files_data:
            files = {"file": (filename, io.BytesIO(content), "text/plain")}
            upload_response = client.post(
                f"/users/{test_user['id']}/files", files=files
            )
            assert upload_response.status_code == 201

        # Download and verify each file
        for filename, expected_content in files_data:
            download_response = client.get(
                f"/users/{test_user['id']}/files/{filename}/download"
            )
            assert download_response.status_code == 200
            assert download_response.content == expected_content

    def test_file_integrity_after_list(self, client, test_user):
        """Test file integrity is maintained after listing files."""
        file_content = b"Test content"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}

        # Upload
        client.post(f"/users/{test_user['id']}/files", files=files)

        # List files
        list_response = client.get(f"/users/{test_user['id']}/files")
        assert list_response.status_code == 200

        # Download and verify
        download_response = client.get(
            f"/users/{test_user['id']}/files/test.txt/download"
        )
        assert download_response.status_code == 200
        assert download_response.content == file_content

    def test_file_integrity_special_characters(self, client, test_user):
        """Test file with special characters in content."""
        # UTF-8 content with special characters
        file_content = "Hello 世界 🌍 café ñoño".encode()
        files = {"file": ("unicode.txt", io.BytesIO(file_content), "text/plain")}

        # Upload
        upload_response = client.post(
            f"/users/{test_user['id']}/files", files=files
        )
        assert upload_response.status_code == 201

        # Download
        download_response = client.get(
            f"/users/{test_user['id']}/files/unicode.txt/download"
        )
        assert download_response.status_code == 200
        assert download_response.content == file_content
