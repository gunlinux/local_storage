"""Shared file management endpoints (no authentication required)."""

from fastapi import APIRouter, HTTPException, UploadFile, status
from fastapi.responses import FileResponse as FastAPIFileResponse

from app.schemas.file import SharedFileResponse, SharedFileUploadResponse
from app.services.shared_file_service import shared_file_service

router = APIRouter(prefix="/shared/files", tags=["shared"])


@router.post("", response_model=SharedFileUploadResponse, status_code=status.HTTP_201_CREATED)
def upload_file(file: UploadFile) -> SharedFileUploadResponse:
    """
    Upload a file to shared storage.

    - **file**: The file to upload

    Returns the uploaded file information.

    Note: No authentication required.
    """
    # Get filename (UploadFile.filename can be None)
    filename = file.filename
    if filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    # Check if file already exists (conflict handling)
    if shared_file_service.file_exists(filename):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"File '{filename}' already exists in shared storage",
        )

    uploaded_file = shared_file_service.upload_file(file)
    if uploaded_file is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to upload file",
        )

    return SharedFileUploadResponse(
        message="File uploaded successfully to shared storage",
        filename=uploaded_file.filename,
    )


@router.get("", response_model=list[SharedFileResponse])
def list_files() -> list[SharedFileResponse]:
    """
    List all shared files.

    Returns a list of all files in shared storage.

    Note: No authentication required.
    """
    files = shared_file_service.list_files()
    return [
        SharedFileResponse(
            id=file.id,
            filename=file.filename,
            created_at=file.created_at,
        )
        for file in files
    ]


@router.get("/{filename}")
def get_file(filename: str) -> SharedFileResponse:
    """
    Get shared file metadata.

    - **filename**: The name of the file

    Returns the file metadata.

    Note: No authentication required.
    """
    file = shared_file_service.get_file(filename)
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    return SharedFileResponse(
        id=file.id,
        filename=file.filename,
        created_at=file.created_at,
    )


@router.get("/{filename}/download")
def download_file(filename: str) -> FastAPIFileResponse:
    """
    Download a file from shared storage.

    - **filename**: The name of the file to download

    Returns the file content for download.

    Note: No authentication required.
    """
    file_path = shared_file_service.download_file(filename)
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
def delete_file(filename: str) -> dict[str, str]:
    """
    Delete a file from shared storage.

    - **filename**: The name of the file to delete

    Returns a success message.

    Note: No authentication required.
    """
    # Check if file exists
    if not shared_file_service.file_exists(filename):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    success = shared_file_service.delete_file(filename)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    return {"message": f"File '{filename}' deleted successfully from shared storage"}
