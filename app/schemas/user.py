"""Pydantic schemas for User."""

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    username: str = Field(..., min_length=1, max_length=50)


class UserResponse(BaseModel):
    """Schema for user response."""

    id: int
    username: str
    created_at: str

    model_config = {"from_attributes": True}
