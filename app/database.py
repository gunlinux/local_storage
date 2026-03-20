"""Database connection and session management using raw SQLite."""

import sqlite3
from collections.abc import Generator
from contextlib import contextmanager

from app.config import BASE_DIR
from app.logging_config import get_logger

logger = get_logger(__name__)

DATABASE_PATH = BASE_DIR / "app" / "storage" / "database.db"


def get_connection() -> sqlite3.Connection:
    """Create and return a database connection."""
    logger.debug(f"Creating database connection to {DATABASE_PATH}")
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_session() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database sessions."""
    logger.debug("Opening database session")
    conn = get_connection()
    try:
        yield conn
        conn.commit()
        logger.debug("Database session committed")
    except Exception as e:
        conn.rollback()
        logger.error(f"Database session rolled back due to error: {e}")
        raise
    finally:
        conn.close()
        logger.debug("Database session closed")


def init_db() -> None:
    """Initialize the database and create tables."""
    logger.info("Initializing database")
    with get_session() as conn:
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        logger.debug("Users table initialized")

        # Create files table for user files
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        logger.debug("Files table initialized")

        # Create shared_files table for public shared storage
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shared_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL UNIQUE,
                filepath TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        logger.debug("Shared files table initialized")

        conn.commit()
        logger.info("Database initialization completed")
