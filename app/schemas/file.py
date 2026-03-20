"""Pydantic schemas for File."""

from pydantic import BaseModel


class FileResponse(BaseModel):
    """Schema for file response."""

    id: int
    user_id: int
    filename: str
    created_at: str

    model_config = {"from_attributes": True}


class FileUploadResponse(BaseModel):
    """Schema for file upload response."""

    message: str
    filename: str
    user_id: int
