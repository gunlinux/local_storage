"""File model with raw SQL queries."""

import sqlite3
from dataclasses import dataclass


@dataclass
class File:
    """File model representing a row in the files table."""

    id: int
    user_id: int
    filename: str
    filepath: str
    created_at: str

    def to_dict(self) -> dict[str, str | int]:
        """Convert file to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "filename": self.filename,
            "filepath": self.filepath,
            "created_at": self.created_at,
        }

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "File":
        """Create File instance from a database row."""
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            filename=row["filename"],
            filepath=row["filepath"],
            created_at=row["created_at"],
        )


class FileRepository:
    """Repository for file-related database operations using raw SQL."""

    @staticmethod
    def create(
        cursor: sqlite3.Cursor, user_id: int, filename: str, filepath: str
    ) -> int | None:
        """
        Create a new file record.

        Returns the file ID if successful, None if file already exists.
        """
        try:
            cursor.execute(
                """
                INSERT INTO files (user_id, filename, filepath)
                VALUES (?, ?, ?)
                """,
                (user_id, filename, filepath),
            )
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, file_id: int) -> "File | None":
        """Get a file by ID."""
        cursor.execute(
            "SELECT id, user_id, filename, filepath, created_at FROM files WHERE id = ?",
            (file_id,),
        )
        row = cursor.fetchone()
        return File.from_row(row) if row else None

    @staticmethod
    def get_by_filename(
        cursor: sqlite3.Cursor, user_id: int, filename: str
    ) -> "File | None":
        """Get a file by filename for a specific user."""
        cursor.execute(
            """
            SELECT id, user_id, filename, filepath, created_at
            FROM files
            WHERE user_id = ? AND filename = ?
            """,
            (user_id, filename),
        )
        row = cursor.fetchone()
        return File.from_row(row) if row else None

    @staticmethod
    def list_by_user(cursor: sqlite3.Cursor, user_id: int) -> list["File"]:
        """List all files for a user."""
        cursor.execute(
            """
            SELECT id, user_id, filename, filepath, created_at
            FROM files
            WHERE user_id = ?
            ORDER BY created_at
            """,
            (user_id,),
        )
        rows = cursor.fetchall()
        return [File.from_row(row) for row in rows]

    @staticmethod
    def delete(cursor: sqlite3.Cursor, file_id: int) -> bool:
        """
        Delete a file record by ID.

        Returns True if file was deleted, False if file not found.
        """
        cursor.execute("DELETE FROM files WHERE id = ?", (file_id,))
        return cursor.rowcount > 0

    @staticmethod
    def delete_by_filename(cursor: sqlite3.Cursor, user_id: int, filename: str) -> bool:
        """
        Delete a file by user_id and filename.

        Returns True if file was deleted, False if file not found.
        """
        cursor.execute(
            "DELETE FROM files WHERE user_id = ? AND filename = ?", (user_id, filename)
        )
        return cursor.rowcount > 0

    @staticmethod
    def exists(cursor: sqlite3.Cursor, file_id: int) -> bool:
        """Check if a file exists by ID."""
        cursor.execute("SELECT 1 FROM files WHERE id = ?", (file_id,))
        return cursor.fetchone() is not None

    @staticmethod
    def file_exists_for_user(
        cursor: sqlite3.Cursor, user_id: int, filename: str
    ) -> bool:
        """Check if a file exists for a user."""
        cursor.execute(
            "SELECT 1 FROM files WHERE user_id = ? AND filename = ?", (user_id, filename)
        )
        return cursor.fetchone() is not None
