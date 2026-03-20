"""Tests for user service CRUD operations."""


import pytest

from app.database import get_session, init_db
from app.models.user import User, UserRepository
from app.schemas.user import UserCreate
from app.services.user_service import UserService


@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    """Set up a test database for each test."""
    # Use a temporary database file
    test_db = tmp_path / "test_database.db"
    monkeypatch.setattr("app.database.DATABASE_PATH", test_db)

    # Initialize the test database
    init_db()
    yield
    # Cleanup
    if test_db.exists():
        test_db.unlink()


@pytest.fixture
def user_service():
    """Provide a UserService instance."""
    return UserService()


class TestUserService:
    """Test cases for UserService."""

    def test_create_user(self, user_service):
        """Test creating a new user."""
        user_data = UserCreate(username="testuser")
        user = user_service.create_user(user_data)

        assert user is not None
        assert user.username == "testuser"
        assert user.id == 1
        assert user.created_at is not None

    def test_create_user_duplicate_username(self, user_service):
        """Test that creating a user with duplicate username fails."""
        user_data = UserCreate(username="testuser")
        user1 = user_service.create_user(user_data)
        assert user1 is not None

        user2 = user_service.create_user(user_data)
        assert user2 is None

    def test_get_user_by_id(self, user_service):
        """Test getting a user by ID."""
        user_data = UserCreate(username="testuser")
        created_user = user_service.create_user(user_data)

        retrieved_user = user_service.get_user(created_user.id)

        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.username == created_user.username

    def test_get_user_by_id_not_found(self, user_service):
        """Test getting a non-existent user by ID."""
        user = user_service.get_user(999)
        assert user is None

    def test_get_user_by_username(self, user_service):
        """Test getting a user by username."""
        user_data = UserCreate(username="testuser")
        created_user = user_service.create_user(user_data)

        retrieved_user = user_service.get_user_by_username("testuser")

        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.username == created_user.username

    def test_get_user_by_username_not_found(self, user_service):
        """Test getting a non-existent user by username."""
        user = user_service.get_user_by_username("nonexistent")
        assert user is None

    def test_list_users(self, user_service):
        """Test listing all users."""
        user_service.create_user(UserCreate(username="user1"))
        user_service.create_user(UserCreate(username="user2"))
        user_service.create_user(UserCreate(username="user3"))

        users = user_service.list_users()

        assert len(users) == 3
        usernames = [u.username for u in users]
        assert "user1" in usernames
        assert "user2" in usernames
        assert "user3" in usernames

    def test_list_users_empty(self, user_service):
        """Test listing users when no users exist."""
        users = user_service.list_users()
        assert len(users) == 0

    def test_delete_user(self, user_service):
        """Test deleting a user."""
        user_data = UserCreate(username="testuser")
        created_user = user_service.create_user(user_data)

        result = user_service.delete_user(created_user.id)
        assert result is True

        # Verify user is deleted
        deleted_user = user_service.get_user(created_user.id)
        assert deleted_user is None

    def test_delete_user_not_found(self, user_service):
        """Test deleting a non-existent user."""
        result = user_service.delete_user(999)
        assert result is False

    def test_user_exists(self, user_service):
        """Test checking if a user exists."""
        user_data = UserCreate(username="testuser")
        created_user = user_service.create_user(user_data)

        assert user_service.user_exists(created_user.id) is True
        assert user_service.user_exists(999) is False


class TestUserRepository:
    """Test cases for UserRepository (raw SQL operations)."""

    def test_create_and_retrieve(self):
        """Test creating and retrieving a user with raw SQL."""
        with get_session() as conn:
            cursor = conn.cursor()

            # Create user
            user_id = UserRepository.create(cursor, "repo_user")
            assert user_id is not None

            # Retrieve by ID
            user = UserRepository.get_by_id(cursor, user_id)
            assert user is not None
            assert user.username == "repo_user"
            assert isinstance(user, User)

    def test_integrity_error_on_duplicate(self):
        """Test that duplicate username raises IntegrityError."""
        with get_session() as conn:
            cursor = conn.cursor()

            # Create first user
            user_id1 = UserRepository.create(cursor, "duplicate_user")
            assert user_id1 is not None

            # Try to create duplicate
            user_id2 = UserRepository.create(cursor, "duplicate_user")
            assert user_id2 is None

    def test_list_all_ordering(self):
        """Test that list_all returns users ordered by created_at."""
        with get_session() as conn:
            cursor = conn.cursor()

            UserRepository.create(cursor, "first_user")
            UserRepository.create(cursor, "second_user")

            users = UserRepository.list_all(cursor)
            assert len(users) == 2
            assert users[0].username == "first_user"
            assert users[1].username == "second_user"

    def test_delete_returns_bool(self):
        """Test that delete returns boolean for success/failure."""
        with get_session() as conn:
            cursor = conn.cursor()

            user_id = UserRepository.create(cursor, "to_delete")
            assert user_id is not None

            # Delete existing user
            result = UserRepository.delete(cursor, user_id)
            assert result is True

            # Try to delete non-existent user
            result = UserRepository.delete(cursor, 999)
            assert result is False

    def test_exists_check(self):
        """Test exists method."""
        with get_session() as conn:
            cursor = conn.cursor()

            user_id = UserRepository.create(cursor, "exists_test")
            assert user_id is not None

            assert UserRepository.exists(cursor, user_id) is True
            assert UserRepository.exists(cursor, 999) is False
