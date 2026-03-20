# API Routes

This document describes the API routes available in the Local File Storage System.

## Base Information

- **Base URL**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)

---

## Health Check

### `GET /health`

Health check endpoint to verify the service is running.

**Response:**
```json
{
  "status": "healthy"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

## User Routes

> **Status**: ✅ Complete

### `POST /users`

Create a new user.

**Request Body:**
```json
{
  "username": "john_doe"
}
```

**Request Schema:** `UserCreate`
- `username` (string, required): 1-50 characters

**Success Response (201 Created):**
```json
{
  "id": 1,
  "username": "john_doe",
  "created_at": "2026-03-20T10:30:00"
}
```

**Error Responses:**
- `400 Bad Request` - Username already exists

---

### `GET /users`

List all users.

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "created_at": "2026-03-20T10:30:00"
  },
  {
    "id": 2,
    "username": "jane_smith",
    "created_at": "2026-03-20T11:00:00"
  }
]
```

---

### `GET /users/{user_id}`

Get a specific user by ID.

**Path Parameters:**
- `user_id` (integer): The user's unique identifier

**Success Response (200 OK):**
```json
{
  "id": 1,
  "username": "john_doe",
  "created_at": "2026-03-20T10:30:00"
}
```

**Error Responses:**
- `404 Not Found` - User not found

---

### `DELETE /users/{user_id}`

Delete a user by ID.

**Path Parameters:**
- `user_id` (integer): The user's unique identifier

**Success Response (200 OK):**
```json
{
  "message": "User 1 deleted successfully"
}
```

**Error Responses:**
- `404 Not Found` - User not found

---

## File Routes

> **Status**: ✅ Complete

### `POST /users/{user_id}/files`

Upload a file for a user.

**Path Parameters:**
- `user_id` (integer): The user's unique identifier

**Request Body:** `multipart/form-data`
- `file` (file, required): The file to upload

**Success Response (201 Created):**
```json
{
  "message": "File uploaded successfully",
  "filename": "document.pdf",
  "user_id": 1
}
```

**Error Responses:**
- `404 Not Found` - User not found
- `409 Conflict` - File already exists for this user
- `400 Bad Request` - Failed to upload file

---

### `GET /users/{user_id}/files`

List all files for a user.

**Path Parameters:**
- `user_id` (integer): The user's unique identifier

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "filename": "document.pdf",
    "created_at": "2026-03-20T11:00:00"
  },
  {
    "id": 2,
    "user_id": 1,
    "filename": "image.png",
    "created_at": "2026-03-20T11:30:00"
  }
]
```

**Error Responses:**
- `404 Not Found` - User not found

---

### `GET /users/{user_id}/files/{filename}`

Get file metadata.

**Path Parameters:**
- `user_id` (integer): The user's unique identifier
- `filename` (string): The name of the file

**Success Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "filename": "document.pdf",
  "created_at": "2026-03-20T11:00:00"
}
```

**Error Responses:**
- `404 Not Found` - User not found or File not found

---

### `GET /users/{user_id}/files/{filename}/download`

Download a file.

**Path Parameters:**
- `user_id` (integer): The user's unique identifier
- `filename` (string): The name of the file

**Success Response (200 OK):**
- Returns the file content with `Content-Type: application/octet-stream`

**Error Responses:**
- `404 Not Found` - User not found or File not found

---

### `DELETE /users/{user_id}/files/{filename}`

Delete a file.

**Path Parameters:**
- `user_id` (integer): The user's unique identifier
- `filename` (string): The name of the file

**Success Response (200 OK):**
```json
{
  "message": "File 'document.pdf' deleted successfully"
}
```

**Error Responses:**
- `404 Not Found` - User not found or File not found

---

## File Storage

Files are stored in the filesystem under `app/storage/users/{user_id}/`.

File metadata is stored in the `files` table with:
- `user_id`: Owner reference
- `filename`: Original file name
- `filepath`: Full path to the stored file

**File Isolation:** Each user has their own storage directory. Files are isolated between users - users cannot access other users' files.

---

## Shared Storage Routes

> **Status**: ✅ Complete

Shared storage is accessible without authentication. Anyone can upload, download, and manage shared files.

### `POST /shared/files`

Upload a file to shared storage.

**Request Body:** `multipart/form-data`
- `file` (file, required): The file to upload

**Success Response (201 Created):**
```json
{
  "message": "File uploaded successfully to shared storage",
  "filename": "document.pdf"
}
```

**Error Responses:**
- `409 Conflict` - File already exists in shared storage
- `400 Bad Request` - Filename is required or Failed to upload file

---

### `GET /shared/files`

List all shared files.

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "filename": "document.pdf",
    "created_at": "2026-03-20T11:00:00"
  },
  {
    "id": 2,
    "filename": "image.png",
    "created_at": "2026-03-20T11:30:00"
  }
]
```

---

### `GET /shared/files/{filename}`

Get shared file metadata.

**Path Parameters:**
- `filename` (string): The name of the file

**Success Response (200 OK):**
```json
{
  "id": 1,
  "filename": "document.pdf",
  "created_at": "2026-03-20T11:00:00"
}
```

**Error Responses:**
- `404 Not Found` - File not found

---

### `GET /shared/files/{filename}/download`

Download a file from shared storage.

**Path Parameters:**
- `filename` (string): The name of the file

**Success Response (200 OK):**
- Returns the file content with `Content-Type: application/octet-stream`

**Error Responses:**
- `404 Not Found` - File not found

---

### `DELETE /shared/files/{filename}`

Delete a file from shared storage.

**Path Parameters:**
- `filename` (string): The name of the file

**Success Response (200 OK):**
```json
{
  "message": "File 'document.pdf' deleted successfully from shared storage"
}
```

**Error Responses:**
- `404 Not Found` - File not found

---

## Shared File Storage

Shared files are stored in the filesystem under `app/storage/shared/`.

File metadata is stored in the `shared_files` table with:
- `filename`: Original file name (unique)
- `filepath`: Full path to the stored file

**Note:** Shared storage is public - no authentication is required for any operations.

---

## Error Response Format

All error responses follow this format:

```json
{
  "detail": "Error message description"
}
```

---

## CORS Configuration

The API is configured to allow access from local network hosts:

- **Allowed Origins**: Configured via `ALLOWED_HOSTS` in `app/config.py`
- **Allowed Methods**: All (`*`)
- **Allowed Headers**: All (`*`)
- **Credentials**: Allowed

---

## Implementation Status

| Route Category    | Status      |
|-------------------|-------------|
| Health Check      | ✅ Complete |
| User Routes       | ✅ Complete |
| File Routes       | ✅ Complete |
| Shared Routes     | ✅ Complete |
