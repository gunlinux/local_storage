"""File service for filesystem operations using repository pattern and raw SQL."""

import shutil
from pathlib import Path

from fastapi import UploadFile

from app.config import USERS_STORAGE_DIR
from app.database import get_session
from app.logging_config import get_logger
from app.models.file import File, FileRepository
from app.services.user_service import user_service

logger = get_logger(__name__)


class FileService:
    """Service layer for file operations using repository pattern."""

    def _get_user_dir(self, user_id: int) -> Path:
        """Get the user's storage directory."""
        user_dir = USERS_STORAGE_DIR / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir

    def _get_file_path(self, user_id: int, filename: str) -> Path:
        """Get the full file path for a user's file."""
        user_dir = self._get_user_dir(user_id)
        return user_dir / filename

    def upload_file(self, user_id: int, file: UploadFile) -> File | None:
        """
        Upload a file for a user.

        Returns the File record if successful, None if file already exists.
        """
        # Validate user exists
        if not user_service.user_exists(user_id):
            logger.warning(f"Upload failed: user {user_id} not found")
            return None

        # Get filename (UploadFile.filename can be None)
        filename = file.filename
        if filename is None:
            logger.warning("Upload failed: filename is None")
            return None

        # Check if file already exists
        with get_session() as conn:
            cursor = conn.cursor()
            if FileRepository.file_exists_for_user(cursor, user_id, filename):
                logger.warning(f"File {filename} already exists for user {user_id}")
                return None

        # Save file to filesystem
        file_path = self._get_file_path(user_id, filename)
        logger.info(f"Uploading file {filename} for user {user_id} to {file_path}")
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Create file record in database
        with get_session() as conn:
            cursor = conn.cursor()
            file_id = FileRepository.create(
                cursor, user_id, filename, str(file_path)
            )
            if file_id is None:
                # Clean up the file if database insert failed
                logger.error(f"Failed to create file record for {filename}, cleaning up")
                file_path.unlink(missing_ok=True)
                return None
            logger.info(f"File {filename} uploaded successfully for user {user_id}")
            return FileRepository.get_by_id(cursor, file_id)

    def list_files(self, user_id: int) -> list[File]:
        """List all files for a user."""
        logger.debug(f"Listing files for user {user_id}")
        with get_session() as conn:
            cursor = conn.cursor()
            return FileRepository.list_by_user(cursor, user_id)

    def get_file(self, user_id: int, filename: str) -> File | None:
        """Get a file by user_id and filename."""
        logger.debug(f"Fetching file {filename} for user {user_id}")
        with get_session() as conn:
            cursor = conn.cursor()
            return FileRepository.get_by_filename(cursor, user_id, filename)

    def download_file(self, user_id: int, filename: str) -> Path | None:
        """
        Get file path for download.

        Returns the file path if file exists, None otherwise.
        """
        logger.debug(f"Preparing file {filename} for download for user {user_id}")
        file = self.get_file(user_id, filename)
        if file is None:
            logger.warning(f"File {filename} not found for user {user_id}")
            return None

        file_path = Path(file.filepath)
        if not file_path.exists():
            logger.error(f"File {filename} exists in database but not on disk for user {user_id}")
            return None

        return file_path

    def delete_file(self, user_id: int, filename: str) -> bool:
        """
        Delete a file.

        Returns True if file was deleted, False if file not found.
        """
        logger.info(f"Deleting file {filename} for user {user_id}")
        with get_session() as conn:
            cursor = conn.cursor()

            # Get file record to know the filepath
            file = FileRepository.get_by_filename(cursor, user_id, filename)
            if file is None:
                logger.warning(f"File {filename} not found for user {user_id}")
                return False

            # Delete from filesystem
            file_path = Path(file.filepath)
            if file_path.exists():
                file_path.unlink()
                logger.debug(f"File {filename} deleted from filesystem")
            else:
                logger.warning(f"File {filename} not found on disk for user {user_id}")

            # Delete from database
            success = FileRepository.delete_by_filename(cursor, user_id, filename)
            if success:
                logger.info(f"File {filename} deleted successfully for user {user_id}")
            return success

    def file_exists(self, user_id: int, filename: str) -> bool:
        """Check if a file exists for a user."""
        logger.debug(f"Checking if file {filename} exists for user {user_id}")
        with get_session() as conn:
            cursor = conn.cursor()
            return FileRepository.file_exists_for_user(cursor, user_id, filename)


# Singleton instance for convenience
file_service = FileService()
