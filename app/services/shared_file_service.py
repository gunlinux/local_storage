"""Shared file service for filesystem operations using repository pattern and raw SQL."""

import shutil
from pathlib import Path

from fastapi import UploadFile

from app.config import SHARED_STORAGE_DIR
from app.database import get_session
from app.logging_config import get_logger
from app.models.shared_file import SharedFile, SharedFileRepository

logger = get_logger(__name__)


class SharedFileService:
    """Service layer for shared file operations using repository pattern."""

    def _get_file_path(self, filename: str) -> Path:
        """Get the full file path for a shared file."""
        return SHARED_STORAGE_DIR / filename

    def upload_file(self, file: UploadFile) -> SharedFile | None:
        """
        Upload a file to shared storage.

        Returns the SharedFile record if successful, None if file already exists.
        """
        # Get filename (UploadFile.filename can be None)
        filename = file.filename
        if filename is None:
            logger.warning("Upload failed: filename is None")
            return None

        # Check if file already exists
        with get_session() as conn:
            cursor = conn.cursor()
            if SharedFileRepository.file_exists(cursor, filename):
                logger.warning(f"File {filename} already exists in shared storage")
                return None

        # Save file to filesystem
        file_path = self._get_file_path(filename)
        logger.info(f"Uploading file {filename} to shared storage at {file_path}")
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Create file record in database
        with get_session() as conn:
            cursor = conn.cursor()
            file_id = SharedFileRepository.create(
                cursor, filename, str(file_path)
            )
            if file_id is None:
                # Clean up the file if database insert failed
                logger.error(f"Failed to create file record for {filename}, cleaning up")
                file_path.unlink(missing_ok=True)
                return None
            logger.info(f"File {filename} uploaded successfully to shared storage")
            return SharedFileRepository.get_by_id(cursor, file_id)

    def list_files(self) -> list[SharedFile]:
        """List all shared files."""
        logger.debug("Listing all shared files")
        with get_session() as conn:
            cursor = conn.cursor()
            return SharedFileRepository.list_all(cursor)

    def get_file(self, filename: str) -> SharedFile | None:
        """Get a shared file by filename."""
        logger.debug(f"Fetching shared file {filename}")
        with get_session() as conn:
            cursor = conn.cursor()
            return SharedFileRepository.get_by_filename(cursor, filename)

    def download_file(self, filename: str) -> Path | None:
        """
        Get file path for download.

        Returns the file path if file exists, None otherwise.
        """
        logger.debug(f"Preparing shared file {filename} for download")
        file = self.get_file(filename)
        if file is None:
            logger.warning(f"Shared file {filename} not found")
            return None

        file_path = Path(file.filepath)
        if not file_path.exists():
            logger.error(f"Shared file {filename} exists in database but not on disk")
            return None

        return file_path

    def delete_file(self, filename: str) -> bool:
        """
        Delete a shared file.

        Returns True if file was deleted, False if file not found.
        """
        logger.info(f"Deleting shared file {filename}")
        with get_session() as conn:
            cursor = conn.cursor()

            # Get file record to know the filepath
            file = SharedFileRepository.get_by_filename(cursor, filename)
            if file is None:
                logger.warning(f"Shared file {filename} not found")
                return False

            # Delete from filesystem
            file_path = Path(file.filepath)
            if file_path.exists():
                file_path.unlink()
                logger.debug(f"Shared file {filename} deleted from filesystem")
            else:
                logger.warning(f"Shared file {filename} not found on disk")

            # Delete from database
            success = SharedFileRepository.delete_by_filename(cursor, filename)
            if success:
                logger.info(f"Shared file {filename} deleted successfully")
            return success

    def file_exists(self, filename: str) -> bool:
        """Check if a shared file exists."""
        logger.debug(f"Checking if shared file {filename} exists")
        with get_session() as conn:
            cursor = conn.cursor()
            return SharedFileRepository.file_exists(cursor, filename)


# Singleton instance for convenience
shared_file_service = SharedFileService()
