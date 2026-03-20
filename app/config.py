import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "app" / "storage"
USERS_STORAGE_DIR = STORAGE_DIR / "users"
SHARED_STORAGE_DIR = STORAGE_DIR / "shared"

# Ensure storage directories exist
USERS_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
SHARED_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# CORS settings for local network access
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")
