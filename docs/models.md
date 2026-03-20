# Database Models

This document describes the database models used in the Local File Storage System.

## Database Technology

- **Database**: SQLite
- **Location**: `app/storage/database.db`
- **Access**: Raw SQL queries (no ORM)

---

## Tables

### `users`

Stores user accounts for the file storage system.

| Column       | Type      | Constraints              | Description                          |
|--------------|-----------|--------------------------|--------------------------------------|
| `id`         | INTEGER   | PRIMARY KEY AUTOINCREMENT| Unique user identifier               |
| `username`   | TEXT      | NOT NULL UNIQUE          | User's username (1-50 characters)    |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP| Account creation timestamp           |

**Example Row:**
```sql
INSERT INTO users (id, username, created_at) 
VALUES (1, 'john_doe', '2026-03-20 10:30:00');
```

---

### `files`

Stores metadata for files uploaded by users.

| Column       | Type      | Constraints              | Description                          |
|--------------|-----------|--------------------------|--------------------------------------|
| `id`         | INTEGER   | PRIMARY KEY AUTOINCREMENT| Unique file identifier               |
| `user_id`    | INTEGER   | NOT NULL                 | Reference to the owning user         |
| `filename`   | TEXT      | NOT NULL                 | Original file name                   |
| `filepath`   | TEXT      | NOT NULL                 | Path to the stored file              |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP| File upload timestamp                |

**Foreign Keys:**
- `user_id` → `users(id)` with `ON DELETE CASCADE`

**Example Row:**
```sql
INSERT INTO files (id, user_id, filename, filepath, created_at) 
VALUES (1, 1, 'document.pdf', 'app/storage/users/1/document.pdf', '2026-03-20 11:00:00');
```

---

## Model Classes

### `User` (Dataclass)

Located in: `app/models/user.py`

```python
@dataclass
class User:
    id: int
    username: str
    created_at: str
```

**Methods:**
- `to_dict()` - Convert user to dictionary
- `from_row(row)` - Create User instance from database row

---

### `UserRepository`

Repository pattern for user database operations.

| Method              | Description                                      | Returns                    |
|---------------------|--------------------------------------------------|----------------------------|
| `create(cursor, username)` | Create a new user                        | `int` (ID) or `None`       |
| `get_by_id(cursor, user_id)` | Get user by ID                         | `User` or `None`           |
| `get_by_username(cursor, username)` | Get user by username            | `User` or `None`           |
| `list_all(cursor)`  | List all users ordered by creation date        | `list[User]`               |
| `delete(cursor, user_id)` | Delete a user by ID                       | `bool`                     |
| `exists(cursor, user_id)` | Check if user exists by ID                | `bool`                     |

---

### `File` (Dataclass)

Located in: `app/models/file.py`

```python
@dataclass
class File:
    id: int
    user_id: int
    filename: str
    filepath: str
    created_at: str
```

**Methods:**
- `to_dict()` - Convert file to dictionary
- `from_row(row)` - Create File instance from database row

---

### `FileRepository`

Repository pattern for file database operations.

| Method              | Description                                      | Returns                    |
|---------------------|--------------------------------------------------|----------------------------|
| `create(cursor, user_id, filename, filepath)` | Create a new file record | `int` (ID) or `None`       |
| `get_by_id(cursor, file_id)` | Get file by ID                         | `File` or `None`           |
| `get_by_filename(cursor, user_id, filename)` | Get file by user and filename | `File` or `None`       |
| `list_by_user(cursor, user_id)` | List all files for a user           | `list[File]`               |
| `delete(cursor, file_id)` | Delete a file by ID                       | `bool`                     |
| `delete_by_filename(cursor, user_id, filename)` | Delete file by user and filename | `bool`        |
| `exists(cursor, file_id)` | Check if file exists by ID                | `bool`                     |
| `file_exists_for_user(cursor, user_id, filename)` | Check if file exists for user | `bool`             |

---

### `SharedFile` (Dataclass)

Located in: `app/models/shared_file.py`

```python
@dataclass
class SharedFile:
    id: int
    filename: str
    filepath: str
    created_at: str
```

**Methods:**
- `to_dict()` - Convert shared file to dictionary
- `from_row(row)` - Create SharedFile instance from database row

---

### `SharedFileRepository`

Repository pattern for shared file database operations.

| Method              | Description                                      | Returns                    |
|---------------------|--------------------------------------------------|----------------------------|
| `create(cursor, filename, filepath)` | Create a new shared file record | `int` (ID) or `None`       |
| `get_by_id(cursor, file_id)` | Get shared file by ID                 | `SharedFile` or `None`     |
| `get_by_filename(cursor, filename)` | Get shared file by filename     | `SharedFile` or `None`     |
| `list_all(cursor)` | List all shared files                           | `list[SharedFile]`         |
| `delete(cursor, file_id)` | Delete a shared file by ID                | `bool`                     |
| `delete_by_filename(cursor, filename)` | Delete shared file by filename | `bool`         |
| `exists(cursor, file_id)` | Check if shared file exists by ID         | `bool`                     |
| `file_exists(cursor, filename)` | Check if shared file exists by filename | `bool`             |

---

## Pydantic Schemas

### `UserCreate`

Schema for creating a new user.

```python
class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
```

### `UserResponse`

Schema for user API responses.

```python
class UserResponse(BaseModel):
    id: int
    username: str
    created_at: str

    model_config = {"from_attributes": True}
```

---

### `FileResponse`

Schema for file API responses.

```python
class FileResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    created_at: str

    model_config = {"from_attributes": True}
```

### `FileUploadResponse`

Schema for file upload API responses.

```python
class FileUploadResponse(BaseModel):
    message: str
    filename: str
    user_id: int
```

---

### `SharedFileResponse`

Schema for shared file API responses.

```python
class SharedFileResponse(BaseModel):
    id: int
    filename: str
    created_at: str

    model_config = {"from_attributes": True}
```

### `SharedFileUploadResponse`

Schema for shared file upload API responses.

```python
class SharedFileUploadResponse(BaseModel):
    message: str
    filename: str
```

---

## Database Initialization

The database is initialized automatically on application startup via `app/database.py`:

```python
def init_db() -> None:
    """Initialize the database and create tables."""
```

This creates `users`, `files`, and `shared_files` tables if they don't exist.

### Tables Created

| Table          | Description                              |
|----------------|------------------------------------------|
| `users`        | User accounts                            |
| `files`        | User file metadata                       |
| `shared_files` | Shared/public file metadata              |
