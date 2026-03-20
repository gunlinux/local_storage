"""User model with raw SQL queries."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import sqlite3


@dataclass
class User:
    """User model representing a row in the users table."""

    id: int
    username: str
    created_at: str

    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at,
        }

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "User":
        """Create User instance from a database row."""
        return cls(
            id=row["id"],
            username=row["username"],
            created_at=row["created_at"],
        )


class UserRepository:
    """Repository for user-related database operations using raw SQL."""

    @staticmethod
    def create(cursor: sqlite3.Cursor, username: str) -> Optional[int]:
        """
        Create a new user.

        Returns the user ID if successful, None if username already exists.
        """
        try:
            cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        cursor.execute(
            "SELECT id, username, created_at FROM users WHERE id = ?", (user_id,)
        )
        row = cursor.fetchone()
        return User.from_row(row) if row else None

    @staticmethod
    def get_by_username(cursor: sqlite3.Cursor, username: str) -> Optional[User]:
        """Get a user by username."""
        cursor.execute(
            "SELECT id, username, created_at FROM users WHERE username = ?", (username,)
        )
        row = cursor.fetchone()
        return User.from_row(row) if row else None

    @staticmethod
    def list_all(cursor: sqlite3.Cursor) -> list[User]:
        """List all users."""
        cursor.execute("SELECT id, username, created_at FROM users ORDER BY created_at")
        rows = cursor.fetchall()
        return [User.from_row(row) for row in rows]

    @staticmethod
    def delete(cursor: sqlite3.Cursor, user_id: int) -> bool:
        """
        Delete a user by ID.

        Returns True if user was deleted, False if user not found.
        """
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        return cursor.rowcount > 0

    @staticmethod
    def exists(cursor: sqlite3.Cursor, user_id: int) -> bool:
        """Check if a user exists by ID."""
        cursor.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone() is not None
