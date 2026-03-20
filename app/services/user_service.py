"""User service with CRUD operations using repository pattern and raw SQL."""


from app.database import get_session
from app.logging_config import get_logger
from app.models.user import User, UserRepository
from app.schemas.user import UserCreate

logger = get_logger(__name__)


class UserService:
    """Service layer for user operations using repository pattern."""

    def create_user(self, user_data: UserCreate) -> User | None:
        """
        Create a new user.

        Returns the created user, or None if username already exists.
        """
        logger.info(f"Creating user: {user_data.username}")
        with get_session() as conn:
            cursor = conn.cursor()
            user_id = UserRepository.create(cursor, user_data.username)
            if user_id is None:
                logger.warning(f"Failed to create user {user_data.username}: username may already exist")
                return None
            logger.info(f"User created successfully with id: {user_id}")
            return UserRepository.get_by_id(cursor, user_id)

    def get_user(self, user_id: int) -> User | None:
        """Get a user by ID."""
        logger.debug(f"Fetching user by id: {user_id}")
        with get_session() as conn:
            cursor = conn.cursor()
            return UserRepository.get_by_id(cursor, user_id)

    def get_user_by_username(self, username: str) -> User | None:
        """Get a user by username."""
        logger.debug(f"Fetching user by username: {username}")
        with get_session() as conn:
            cursor = conn.cursor()
            return UserRepository.get_by_username(cursor, username)

    def list_users(self) -> list[User]:
        """List all users."""
        logger.debug("Fetching all users")
        with get_session() as conn:
            cursor = conn.cursor()
            return UserRepository.list_all(cursor)

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user by ID.

        Returns True if user was deleted, False if user not found.
        """
        logger.info(f"Deleting user with id: {user_id}")
        with get_session() as conn:
            cursor = conn.cursor()
            success = UserRepository.delete(cursor, user_id)
            if success:
                logger.info(f"User {user_id} deleted successfully")
            else:
                logger.warning(f"User {user_id} not found for deletion")
            return success

    def user_exists(self, user_id: int) -> bool:
        """Check if a user exists by ID."""
        logger.debug(f"Checking if user exists: {user_id}")
        with get_session() as conn:
            cursor = conn.cursor()
            return UserRepository.exists(cursor, user_id)


# Singleton instance for convenience
user_service = UserService()
