"""Shared file service for filesystem operations using repository pattern and raw SQL."""

import shutil
from pathlib import Path

from fastapi import UploadFile

from app.config import SHARED_STORAGE_DIR
from app.database import get_session
from app.models.shared_file import SharedFile, SharedFileRepository


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
            return None

        # Check if file already exists
        with get_session() as conn:
            cursor = conn.cursor()
            if SharedFileRepository.file_exists(cursor, filename):
                return None

        # Save file to filesystem
        file_path = self._get_file_path(filename)
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
                file_path.unlink(missing_ok=True)
                return None
            return SharedFileRepository.get_by_id(cursor, file_id)

    def list_files(self) -> list[SharedFile]:
        """List all shared files."""
        with get_session() as conn:
            cursor = conn.cursor()
            return SharedFileRepository.list_all(cursor)

    def get_file(self, filename: str) -> SharedFile | None:
        """Get a shared file by filename."""
        with get_session() as conn:
            cursor = conn.cursor()
            return SharedFileRepository.get_by_filename(cursor, filename)

    def download_file(self, filename: str) -> Path | None:
        """
        Get file path for download.

        Returns the file path if file exists, None otherwise.
        """
        file = self.get_file(filename)
        if file is None:
            return None

        file_path = Path(file.filepath)
        if not file_path.exists():
            return None

        return file_path

    def delete_file(self, filename: str) -> bool:
        """
        Delete a shared file.

        Returns True if file was deleted, False if file not found.
        """
        with get_session() as conn:
            cursor = conn.cursor()

            # Get file record to know the filepath
            file = SharedFileRepository.get_by_filename(cursor, filename)
            if file is None:
                return False

            # Delete from filesystem
            file_path = Path(file.filepath)
            if file_path.exists():
                file_path.unlink()

            # Delete from database
            return SharedFileRepository.delete_by_filename(cursor, filename)

    def file_exists(self, filename: str) -> bool:
        """Check if a shared file exists."""
        with get_session() as conn:
            cursor = conn.cursor()
            return SharedFileRepository.file_exists(cursor, filename)


# Singleton instance for convenience
shared_file_service = SharedFileService()
