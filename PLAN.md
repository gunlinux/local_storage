# MVP Implementation Plan: Local File Storage System

## Project Overview

A FastAPI-based local file storage system that allows user management, per-user file storage, and network-shared storage access without password authentication.

---

## MVP Scope

### Core Features (MVP)
1. **User Management**
   - Create users
   - List users
   - Delete users

2. **File Storage (Per-User)**
   - Upload files to user's storage
   - Download files
   - List user's files
   - Delete files

3. **Shared Storage**
   - Public shared folder accessible without authentication
   - Upload/download files to shared storage
   - List shared files

4. **Network Sharing**
   - Serve files over local network
   - CORS configuration for network access

### Out of Scope (Post-MVP)
- User authentication/passwords
- File permissions and access control
- File versioning
- Search functionality
- File preview/thumbnails
- User quotas/storage limits
- Database persistence (use SQLite for MVP)
- use RAW SQL
- dont use ORM

---

## Technical Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Database | PostgreSQL (without ORM) |
| File Storage | Local filesystem |
| Validation | Pydantic |
| Server | Uvicorn |

---

## Project Structure

```
some_project/
├── pyproject.toml          # Project config & dependencies
├── README.md
├── PLAN.md
├── .env                    # Environment variables (optional)
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI app entry point
│   ├── config.py           # Configuration settings
│   ├── database.py         # Database setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py         # User model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py         # Pydantic schemas for users
│   │   └── file.py         # Pydantic schemas for files
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py        # User endpoints
│   │   ├── files.py        # User file endpoints
│   │   └── shared.py       # Shared storage endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── file_service.py
│   └── storage/            # File storage location
│       ├── users/          # Per-user folders
│       └── shared/         # Shared storage folder
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_users.py
    ├── test_files.py
    └── test_shared.py
```

---

## Implementation Phases

### Phase 1: Project Setup
**Goal:** Initialize project structure and dependencies

- [x] Create `pyproject.toml` with dependencies:
  - `fastapi`
  - `uvicorn[standard]`
  - `python-multipart`
  - `pydantic`
  - `pytest` (dev)
  - `httpx` (dev, for testing)
- [x] Create project directory structure
- [x] Set up virtual environment
- [x] Create basic `app/main.py` with health check endpoint
- [x] Configure CORS for local network access

**Deliverable:** Running FastAPI app with `/health` endpoint ✅

---

### Phase 2: Database & User Model
**Goal:** Persistent user storage

- [x] Set up SQLite database
- [x] Create `User` model (id, username, created_at)
- [x] Create database session management
- [x] Implement user CRUD operations in `user_service.py`

**Deliverable:** Working database with user management ✅

---

### Phase 3: User Management API
**Goal:** RESTful user endpoints

- [x] Create Pydantic schemas for User (create, response)
- [x] Implement `/users` endpoints:
  - `POST /users` - Create user
  - `GET /users` - List all users
  - `GET /users/{user_id}` - Get user details
  - `DELETE /users/{user_id}` - Delete user
- [x] Add error handling (duplicate username, not found)

**Deliverable:** Complete user management API ✅

---

### Phase 4: User File Storage API
**Goal:** Per-user file upload/download

- [x] Create file service for filesystem operations
- [x] Implement file endpoints:
  - `POST /users/{user_id}/files` - Upload file
  - `GET /users/{user_id}/files` - List files
  - `GET /users/{user_id}/files/{filename}` - Get file info
  - `GET /users/{user_id}/files/{filename}/download` - Download file
  - `DELETE /users/{user_id}/files/{filename}` - Delete file
- [x] Handle file metadata (store in DB or derive from filesystem)
- [x] Validate file ownership (user exists)
- [x] Handle file conflicts (duplicate names)

**Deliverable:** Working per-user file storage ✅

---

### Phase 5: Shared Storage API
**Goal:** Password-free shared storage

- [x] Create shared storage directory structure
- [x] Implement shared endpoints:
  - `POST /shared/files` - Upload file
  - `GET /shared/files` - List all shared files
  - `GET /shared/files/{filename}` - Get file info
  - `GET /shared/files/{filename}/download` - Download file
  - `DELETE /shared/files/{filename}` - Delete file
- [x] No authentication required for these endpoints

**Deliverable:** Public shared storage accessible without auth ✅

---

### Phase 6: Testing
**Goal:** Ensure reliability

- [x] Set up pytest configuration
- [x] Create test fixtures (test database, temp directories)
- [x] Write tests for user endpoints
- [x] Write tests for file endpoints
- [x] Write tests for shared storage endpoints
- [x] Test file upload/download integrity

**Deliverable:** Test suite with >80% coverage ✅

---

### Phase 7: Documentation & Polish
**Goal:** Usable and documented API

- [x] Add API documentation (FastAPI auto-generated OpenAPI/Swagger)
- [x] Add README with:
  - Installation instructions
  - How to run the server
  - API usage examples
  - Network access instructions
- [x] Add environment configuration options
- [x] Error message improvements
- [x] Logging setup

**Deliverable:** Production-ready MVP ✅

---

## API Endpoints Summary

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users` | Create a new user |
| GET | `/users` | List all users |
| GET | `/users/{user_id}` | Get user details |
| DELETE | `/users/{user_id}` | Delete a user |

### User Files
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/{user_id}/files` | Upload a file |
| GET | `/users/{user_id}/files` | List user's files |
| GET | `/users/{user_id}/files/{filename}` | Get file info |
| GET | `/users/{user_id}/files/{filename}/download` | Download a file |
| DELETE | `/users/{user_id}/files/{filename}` | Delete a file |

### Shared Storage
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/shared/files` | Upload to shared storage |
| GET | `/shared/files` | List shared files |
| GET | `/shared/files/{filename}` | Get file info |
| GET | `/shared/files/{filename}/download` | Download from shared |
| DELETE | `/shared/files/{filename}` | Delete shared file |

### System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |

---

## Success Criteria

- [x] All endpoints functional and tested
- [x] Files can be uploaded and downloaded successfully
- [x] Multiple users can coexist with isolated storage
- [x] Shared storage accessible without authentication
- [x] Server accessible from other devices on local network
- [x] All tests passing (68 tests)
- [x] Clear documentation for setup and usage

---


## Notes

- Keep implementation simple and focused on MVP
- Use filesystem for file storage (no cloud/S3 for MVP)
- SQLite is sufficient for MVP (no PostgreSQL/MySQL needed yet)
- No authentication for MVP (as per requirements: "password-free access")
- CORS must be configured for network sharing to work properly
