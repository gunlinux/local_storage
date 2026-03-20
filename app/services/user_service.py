"""User service with CRUD operations using repository pattern and raw SQL."""


from app.database import get_session
from app.models.user import User, UserRepository
from app.schemas.user import UserCreate


class UserService:
    """Service layer for user operations using repository pattern."""

    def create_user(self, user_data: UserCreate) -> User | None:
        """
        Create a new user.

        Returns the created user, or None if username already exists.
        """
        with get_session() as conn:
            cursor = conn.cursor()
            user_id = UserRepository.create(cursor, user_data.username)
            if user_id is None:
                return None
            return UserRepository.get_by_id(cursor, user_id)

    def get_user(self, user_id: int) -> User | None:
        """Get a user by ID."""
        with get_session() as conn:
            cursor = conn.cursor()
            return UserRepository.get_by_id(cursor, user_id)

    def get_user_by_username(self, username: str) -> User | None:
        """Get a user by username."""
        with get_session() as conn:
            cursor = conn.cursor()
            return UserRepository.get_by_username(cursor, username)

    def list_users(self) -> list[User]:
        """List all users."""
        with get_session() as conn:
            cursor = conn.cursor()
            return UserRepository.list_all(cursor)

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user by ID.

        Returns True if user was deleted, False if user not found.
        """
        with get_session() as conn:
            cursor = conn.cursor()
            return UserRepository.delete(cursor, user_id)

    def user_exists(self, user_id: int) -> bool:
        """Check if a user exists by ID."""
        with get_session() as conn:
            cursor = conn.cursor()
            return UserRepository.exists(cursor, user_id)


# Singleton instance for convenience
user_service = UserService()
