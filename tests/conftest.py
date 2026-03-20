"""Pytest configuration and shared fixtures."""

import io

import pytest
from fastapi.testclient import TestClient

from app.database import init_db
from app.main import app


@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    """
    Set up a test database and storage for each test.

    This fixture is automatically used by all tests. It creates:
    - A temporary SQLite database
    - Temporary storage directories for users and shared files

    Args:
        tmp_path: Pytest temporary path fixture
        monkeypatch: Pytest monkeypatch fixture
    """
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
    """
    Provide a test client for making HTTP requests.

    Returns:
        TestClient: FastAPI test client
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_user(client):
    """
    Create a test user and return user info.

    Returns:
        dict: User data including id, username, and created_at
    """
    response = client.post("/users", json={"username": "testuser"})
    return response.json()


@pytest.fixture
def sample_file_content():
    """
    Provide sample file content for testing.

    Returns:
        bytes: Sample file content
    """
    return b"Hello, World! This is test file content."


@pytest.fixture
def sample_file(sample_file_content):
    """
    Create a sample file for upload testing.

    Returns:
        dict: Files dict ready for multipart form upload
    """
    return {"file": ("test.txt", io.BytesIO(sample_file_content), "text/plain")}


@pytest.fixture
def large_file_content():
    """
    Provide large file content for testing file integrity.

    Returns:
        bytes: Large file content (1MB)
    """
    return b"x" * (1024 * 1024)  # 1MB of data


@pytest.fixture
def binary_file_content():
    """
    Provide binary file content for testing.

    Returns:
        bytes: Binary file content (simulating an image)
    """
    # Simple PNG header simulation
    return b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
