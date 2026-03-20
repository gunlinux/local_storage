"""User management endpoints."""

from fastapi import APIRouter, HTTPException, status

from app.logging_config import get_logger
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import user_service

logger = get_logger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate) -> UserResponse:
    """
    Create a new user.

    - **username**: Unique username (1-50 characters)

    Returns the created user data.
    """
    logger.info(f"Create user request received for username: {user_data.username}")
    
    # Check if username already exists
    existing_user = user_service.get_user_by_username(user_data.username)
    if existing_user:
        logger.warning(f"Create user failed: username '{user_data.username}' already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    created_user = user_service.create_user(user_data)
    if created_user is None:
        logger.error(f"Create user failed for username '{user_data.username}': service returned None")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create user",
        )

    logger.info(f"User created successfully: {created_user.username} (id={created_user.id})")
    return UserResponse(
        id=created_user.id,
        username=created_user.username,
        created_at=created_user.created_at,
    )


@router.get("", response_model=list[UserResponse])
def list_users() -> list[UserResponse]:
    """
    List all users.

    Returns a list of all registered users.
    """
    logger.debug("List users request received")
    users = user_service.list_users()
    logger.info(f"Listed {len(users)} users")
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            created_at=user.created_at,
        )
        for user in users
    ]


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int) -> UserResponse:
    """
    Get user details by ID.

    - **user_id**: The unique identifier of the user
    """
    logger.debug(f"Get user request received for user_id: {user_id}")
    user = user_service.get_user(user_id)
    if user is None:
        logger.warning(f"Get user failed: user {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    logger.info(f"User {user_id} retrieved successfully")
    return UserResponse(
        id=user.id,
        username=user.username,
        created_at=user.created_at,
    )


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int) -> dict[str, str]:
    """
    Delete a user by ID.

    - **user_id**: The unique identifier of the user to delete
    """
    logger.info(f"Delete user request received for user_id: {user_id}")
    
    if not user_service.user_exists(user_id):
        logger.warning(f"Delete user failed: user {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    success = user_service.delete_user(user_id)
    if not success:
        logger.error(f"Delete user failed for user {user_id}: service returned False")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    logger.info(f"User {user_id} deleted successfully")
    return {"message": f"User {user_id} deleted successfully"}
