"""File management endpoints for user files."""

from fastapi import APIRouter, HTTPException, UploadFile, status
from fastapi.responses import FileResponse as FastAPIFileResponse

from app.logging_config import get_logger
from app.schemas.file import FileResponse, FileUploadResponse
from app.services.file_service import file_service
from app.services.user_service import user_service

logger = get_logger(__name__)

router = APIRouter(prefix="/users/{user_id}/files", tags=["files"])


@router.post("", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
def upload_file(user_id: int, file: UploadFile) -> FileUploadResponse:
    """
    Upload a file to user's storage.

    - **user_id**: The unique identifier of the user
    - **file**: The file to upload

    Returns the uploaded file information.
    """
    logger.info(f"Upload file request received for user {user_id}, file: {file.filename or 'unknown'}")

    # Validate user exists
    if not user_service.user_exists(user_id):
        logger.warning(f"Upload file failed: user {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Get filename (UploadFile.filename can be None)
    filename = file.filename
    if filename is None:
        logger.warning("Upload file failed: filename is None")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    # Check if file already exists (conflict handling)
    if file_service.file_exists(user_id, filename):
        logger.warning(f"Upload file failed: file '{filename}' already exists for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"File '{filename}' already exists for this user",
        )

    uploaded_file = file_service.upload_file(user_id, file)
    if uploaded_file is None:
        logger.error(f"Upload file failed for user {user_id}, file '{filename}': service returned None")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to upload file",
        )

    logger.info(f"File '{filename}' uploaded successfully for user {user_id}")
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
    logger.debug(f"List files request received for user {user_id}")

    # Validate user exists
    if not user_service.user_exists(user_id):
        logger.warning(f"List files failed: user {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    files = file_service.list_files(user_id)
    logger.info(f"Listed {len(files)} files for user {user_id}")
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
    logger.debug(f"Get file info request received for user {user_id}, file: {filename}")

    # Validate user exists
    if not user_service.user_exists(user_id):
        logger.warning(f"Get file info failed: user {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Get file
    file = file_service.get_file(user_id, filename)
    if file is None:
        logger.warning(f"Get file info failed: file '{filename}' not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    logger.info(f"File '{filename}' info retrieved for user {user_id}")
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
    logger.info(f"Download file request received for user {user_id}, file: {filename}")

    # Validate user exists
    if not user_service.user_exists(user_id):
        logger.warning(f"Download file failed: user {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    file_path = file_service.download_file(user_id, filename)
    if file_path is None:
        logger.warning(f"Download file failed: file '{filename}' not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    logger.info(f"File '{filename}' downloaded successfully for user {user_id}")
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
    logger.info(f"Delete file request received for user {user_id}, file: {filename}")

    # Validate user exists
    if not user_service.user_exists(user_id):
        logger.warning(f"Delete file failed: user {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Check if file exists
    if not file_service.file_exists(user_id, filename):
        logger.warning(f"Delete file failed: file '{filename}' not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    success = file_service.delete_file(user_id, filename)
    if not success:
        logger.error(f"Delete file failed for user {user_id}, file '{filename}': service returned False")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    logger.info(f"File '{filename}' deleted successfully for user {user_id}")
    return {"message": f"File '{filename}' deleted successfully"}
