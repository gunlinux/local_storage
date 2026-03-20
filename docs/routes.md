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

> **Note**: File storage routes are pending implementation.

### Planned Endpoints

| Method | Endpoint              | Description                    |
|--------|-----------------------|--------------------------------|
| `POST` | `/users/{user_id}/files` | Upload a file for a user    |
| `GET`  | `/users/{user_id}/files` | List files for a user       |
| `GET`  | `/users/{user_id}/files/{file_id}` | Get file metadata |
| `GET`  | `/files/{file_id}/download` | Download a file          |
| `DELETE` | `/users/{user_id}/files/{file_id}` | Delete a file   |

---

## Shared Storage Routes

> **Note**: Shared/public storage routes are pending implementation.

### Planned Endpoints

| Method | Endpoint              | Description                    |
|--------|-----------------------|--------------------------------|
| `GET`  | `/shared/files`       | List all shared files          |
| `POST` | `/shared/files`       | Upload a shared file           |
| `GET`  | `/shared/files/{file_id}/download` | Download shared file |
| `DELETE` | `/shared/files/{file_id}` | Delete a shared file     |

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
| File Routes       | ⏳ Pending  |
| Shared Routes     | ⏳ Pending  |
