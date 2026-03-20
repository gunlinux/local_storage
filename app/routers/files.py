"""File management endpoints for user files."""

from fastapi import APIRouter, HTTPException, UploadFile, status
from fastapi.responses import FileResponse as FastAPIFileResponse

from app.schemas.file import FileResponse, FileUploadResponse
from app.services.file_service import file_service
from app.services.user_service import user_service

router = APIRouter(prefix="/users/{user_id}/files", tags=["files"])


@router.post("", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
def upload_file(user_id: int, file: UploadFile) -> FileUploadResponse:
    """
    Upload a file to user's storage.

    - **user_id**: The unique identifier of the user
    - **file**: The file to upload

    Returns the uploaded file information.
    """
    # Validate user exists
    if not user_service.user_exists(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Get filename (UploadFile.filename can be None)
    filename = file.filename
    if filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    # Check if file already exists (conflict handling)
    if file_service.file_exists(user_id, filename):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"File '{filename}' already exists for this user",
        )

    uploaded_file = file_service.upload_file(user_id, file)
    if uploaded_file is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to upload file",
        )

    return FileUploadResponse(
        message="File uploaded successfully",
        filename=uploaded_file.filename,
        user_id=uploaded_file.user_id,
    )


@router.get("", response_model=list[FileResponse])
def list_files(user_id: int) -> list[FileResponse]:
    """
    List all files for a user.

    - **user_id**: The unique identifier of the user

    Returns a list of all files owned by the user.
    """
    # Validate user exists
    if not user_service.user_exists(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    files = file_service.list_files(user_id)
    return [
        FileResponse(
            id=file.id,
            user_id=file.user_id,
            filename=file.filename,
            created_at=file.created_at,
        )
        for file in files
    ]


@router.get("/{filename}")
def download_file(user_id: int, filename: str) -> FileResponse:
    """
    Download a file.

    - **user_id**: The unique identifier of the user
    - **filename**: The name of the file to download

    Returns the file for download.
    """
    # Validate user exists
    if not user_service.user_exists(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Get file
    file = file_service.get_file(user_id, filename)
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    return FileResponse(
        id=file.id,
        user_id=file.user_id,
        filename=file.filename,
        created_at=file.created_at,
    )


@router.get("/{filename}/download")
def download_file_direct(user_id: int, filename: str) -> FastAPIFileResponse:
    """
    Download a file directly (returns file content).

    - **user_id**: The unique identifier of the user
    - **filename**: The name of the file to download

    Returns the file content for download.
    """
    # Validate user exists
    if not user_service.user_exists(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    file_path = file_service.download_file(user_id, filename)
    if file_path is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    return FastAPIFileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
    )


@router.delete("/{filename}", status_code=status.HTTP_200_OK)
def delete_file(user_id: int, filename: str) -> dict[str, str]:
    """
    Delete a file.

    - **user_id**: The unique identifier of the user
    - **filename**: The name of the file to delete

    Returns a success message.
    """
    # Validate user exists
    if not user_service.user_exists(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Check if file exists
    if not file_service.file_exists(user_id, filename):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    success = file_service.delete_file(user_id, filename)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    return {"message": f"File '{filename}' deleted successfully"}
