# Project Context: some_project

## Project Overview

This is a **FastAPI (Python)** project that implements a **local file storage system** designed to be shared across a local network.

### Key Features
- User creation and management
- File storage per user (isolated)
- Network-shared storage access
- Password-free access for shared storage
- RESTful API with full CRUD operations

## Current State

**✅ MVP Complete - All Phases (1-7)**

### Implementation Progress

| Phase | Component | Status |
|-------|-----------|--------|
| Phase 1 | Project Setup | ✅ Complete |
| Phase 2 | Database & User Model | ✅ Complete |
| Phase 3 | User Management API | ✅ Complete |
| Phase 4 | User File Storage API | ✅ Complete |
| Phase 5 | Shared Storage API | ✅ Complete |
| Phase 6 | Testing | ✅ Complete (68 tests passing) |
| Phase 7 | Documentation & Polish | ✅ Complete |

### Test Status
- **Total Tests**: 68 passing
- **Coverage**: User endpoints, File endpoints, Shared endpoints, Services, File integrity

### Quality Assurance
- **Linting**: ruff ✅
- **Type Checking**: mypy ✅
- **Tests**: pytest (68 tests) ✅

## Project Structure

```
some_project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection (SQLite, raw SQL)
│   ├── logging_config.py    # Logging configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model (dataclass + repository)
│   │   ├── file.py          # File model (dataclass + repository)
│   │   └── shared_file.py   # SharedFile model (dataclass + repository)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # User Pydantic schemas
│   │   └── file.py          # File Pydantic schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py         # User endpoints
│   │   ├── files.py         # User file endpoints
│   │   └── shared.py        # Shared storage endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py  # User business logic
│   │   ├── file_service.py  # File business logic
│   │   └── shared_file_service.py  # Shared file business logic
│   └── storage/
│       ├── database.db      # SQLite database
│       ├── users/           # Per-user file storage
│       └── shared/          # Shared public storage
├── docs/
│   ├── models.md            # Database models documentation
│   └── routes.md            # API routes documentation
├── logs/
│   └── app.log              # Application logs
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Shared pytest fixtures
│   ├── test_users.py      # User endpoint tests
│   ├── test_files.py      # File endpoint tests (19 tests)
│   ├── test_shared.py     # Shared endpoint tests (12 tests)
│   ├── test_user_service.py # User service tests
│   └── test_file_integrity.py # File integrity tests (10 tests)
├── .env.example           # Example environment configuration
├── pyproject.toml
├── README.md
├── PLAN.md                  # Implementation plan
├── PHASE04.md               # Phase 4 completion summary
├── PHASE05.md               # Phase 5 completion summary
├── PHASE07.md               # Phase 7 completion summary
└── QWEN.md
```

## Dependencies

### Runtime
- `fastapi>=0.104.0`
- `uvicorn[standard]>=0.24.0`
- `python-multipart>=0.0.6`
- `pydantic>=2.0.0`

### Dev
- `pytest>=7.4.0`
- `httpx>=0.25.0`
- `ruff>=0.1.0`
- `mypy>=1.7.0`

### Build
- `hatchling`

## Database Schema

### Tables

| Table          | Description                              |
|----------------|------------------------------------------|
| `users`        | User accounts (id, username, created_at) |
| `files`        | User file metadata (id, user_id, filename, filepath, created_at) |
| `shared_files` | Shared file metadata (id, filename, filepath, created_at) |

**Location:** `app/storage/database.db`

**Access:** Raw SQL queries (no ORM)

## API Endpoints

### System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |

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

## Building and Running

### Setup
```bash
source .venv/bin/activate
```

### Run Server
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The server will be available at:
- Local: `http://localhost:8000`
- Network: `http://<your-ip>:8000`
- API Docs: `http://localhost:8000/docs`

### Run Tests
```bash
uv run pytest
```

### Quality Assurance
```bash
make qa  # Runs lint, type-check, and tests
```

## Development Conventions

- **No SQLAlchemy** - Use raw SQL with repository pattern
- **Pydantic v2** for schemas/validation
- **Hatchling** as build backend
- **Python 3.10+** required
- **Linting**: ruff with line-length 88
- **Type checking**: mypy in strict mode
- **Logging**: Centralized logging to console and `logs/app.log`
- **Environment**: Configuration via `.env` file (see `.env.example`)
- **On every database models change** - update `docs/models.md`
- **On every route change** - update `docs/routes.md`
- **Do not run Development server or curl for test** - write pytest tests and execute using `make test`

## Architecture Patterns

### Repository Pattern
All database operations use the repository pattern with raw SQL:
- `UserRepository` - User CRUD operations
- `FileRepository` - User file CRUD operations
- `SharedFileRepository` - Shared file CRUD operations

### Service Layer
Business logic is encapsulated in service classes:
- `UserService` - User operations
- `FileService` - User file operations
- `SharedFileService` - Shared file operations

### Logging
Centralized logging configuration with console and file handlers:
- **Configuration**: `app/logging_config.py`
- **Log file**: `logs/app.log`
- **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Configured via**: `LOG_LEVEL` environment variable

### File Storage
- **User files**: `app/storage/users/{user_id}/{filename}`
- **Shared files**: `app/storage/shared/{filename}`

### Environment Configuration
- **File**: `.env` (copy from `.env.example`)
- **Variables**: `LOG_LEVEL`, `ALLOWED_HOSTS`, `HOST`, `PORT`

## Qwen Added Memories
- /Users/loki/llm/fastapi.md
- docs/models.md
- docs/routes.md
- PLAN.md
