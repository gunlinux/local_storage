"""User management endpoints."""

from fastapi import APIRouter, HTTPException, status

from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate) -> UserResponse:
    """
    Create a new user.

    - **username**: Unique username (1-50 characters)

    Returns the created user data.
    """
    # Check if username already exists
    existing_user = user_service.get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    created_user = user_service.create_user(user_data)
    if created_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create user",
        )

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
    users = user_service.list_users()
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
    user = user_service.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

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
    if not user_service.user_exists(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return {"message": f"User {user_id} deleted successfully"}
