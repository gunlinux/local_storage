"""Shared file model with raw SQL queries."""

import sqlite3
from dataclasses import dataclass


@dataclass
class SharedFile:
    """Shared file model representing a row in the shared_files table."""

    id: int
    filename: str
    filepath: str
    created_at: str

    def to_dict(self) -> dict[str, str | int]:
        """Convert shared file to dictionary."""
        return {
            "id": self.id,
            "filename": self.filename,
            "filepath": self.filepath,
            "created_at": self.created_at,
        }

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "SharedFile":
        """Create SharedFile instance from a database row."""
        return cls(
            id=row["id"],
            filename=row["filename"],
            filepath=row["filepath"],
            created_at=row["created_at"],
        )


class SharedFileRepository:
    """Repository for shared file-related database operations using raw SQL."""

    @staticmethod
    def create(
        cursor: sqlite3.Cursor, filename: str, filepath: str
    ) -> int | None:
        """
        Create a new shared file record.

        Returns the file ID if successful, None if file already exists.
        """
        try:
            cursor.execute(
                """
                INSERT INTO shared_files (filename, filepath)
                VALUES (?, ?)
                """,
                (filename, filepath),
            )
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, file_id: int) -> "SharedFile | None":
        """Get a shared file by ID."""
        cursor.execute(
            "SELECT id, filename, filepath, created_at FROM shared_files WHERE id = ?",
            (file_id,),
        )
        row = cursor.fetchone()
        return SharedFile.from_row(row) if row else None

    @staticmethod
    def get_by_filename(cursor: sqlite3.Cursor, filename: str) -> "SharedFile | None":
        """Get a shared file by filename."""
        cursor.execute(
            """
            SELECT id, filename, filepath, created_at
            FROM shared_files
            WHERE filename = ?
            """,
            (filename,),
        )
        row = cursor.fetchone()
        return SharedFile.from_row(row) if row else None

    @staticmethod
    def list_all(cursor: sqlite3.Cursor) -> list["SharedFile"]:
        """List all shared files."""
        cursor.execute(
            """
            SELECT id, filename, filepath, created_at
            FROM shared_files
            ORDER BY created_at
            """,
        )
        rows = cursor.fetchall()
        return [SharedFile.from_row(row) for row in rows]

    @staticmethod
    def delete(cursor: sqlite3.Cursor, file_id: int) -> bool:
        """
        Delete a shared file record by ID.

        Returns True if file was deleted, False if file not found.
        """
        cursor.execute("DELETE FROM shared_files WHERE id = ?", (file_id,))
        return cursor.rowcount > 0

    @staticmethod
    def delete_by_filename(cursor: sqlite3.Cursor, filename: str) -> bool:
        """
        Delete a shared file by filename.

        Returns True if file was deleted, False if file not found.
        """
        cursor.execute("DELETE FROM shared_files WHERE filename = ?", (filename,))
        return cursor.rowcount > 0

    @staticmethod
    def exists(cursor: sqlite3.Cursor, file_id: int) -> bool:
        """Check if a shared file exists by ID."""
        cursor.execute("SELECT 1 FROM shared_files WHERE id = ?", (file_id,))
        return cursor.fetchone() is not None

    @staticmethod
    def file_exists(cursor: sqlite3.Cursor, filename: str) -> bool:
        """Check if a shared file exists by filename."""
        cursor.execute("SELECT 1 FROM shared_files WHERE filename = ?", (filename,))
        return cursor.fetchone() is not None
