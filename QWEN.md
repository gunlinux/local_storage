# Project Context: some_project

## Project Overview

This is a **FastAPI (Python)** project that implements a **local file storage system** designed to be shared across a local network.

### Key Features
- User creation and management
- File storage per user
- Network-shared storage access
- Password-free access for shared storage

## Current State

**✅ Project Initialized with Documentation**

The project has been set up with the following structure:

### Dependencies (`pyproject.toml`)
- **Runtime**: fastapi>=0.104.0, uvicorn[standard]>=0.24.0, python-multipart>=0.0.6, pydantic>=2.0.0
- **Dev**: pytest>=7.4.0, httpx>=0.25.0, ruff>=0.1.0, mypy>=1.7.0
- **Build**: hatchling

### Project Structure
```
some_project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection (SQLite, raw SQL)
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # User model (dataclass + repository)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py          # User Pydantic schemas
│   ├── routers/
│   │   └── __init__.py      # API routers (placeholder)
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py  # User business logic
│   └── storage/
│       ├── users/           # Per-user file storage
│       └── shared/          # Shared public storage
├── docs/
│   ├── models.md            # Database models documentation
│   └── routes.md            # API routes documentation
├── tests/
│   ├── __init__.py
│   └── test_user_service.py # User service tests
├── pyproject.toml
├── README.md
└── QWEN.md
```

### Database Schema

**Tables:**
- `users` - User accounts (id, username, created_at)
- `files` - File metadata (id, user_id, filename, filepath, created_at)

**Location:** `app/storage/database.db`

**Access:** Raw SQL queries (no ORM)

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

## Development Conventions

- **No SQLAlchemy** - Use alternative database approaches
- **Pydantic v2** for schemas/validation
- **Hatchling** as build backend
- **Python 3.10+** required
- **Linting**: ruff with line-length 88
- **Type checking**: mypy in strict mode
- **On every database models change - update docs/models.md**
- **On every route change - update docs/routes.md**
- **Do not run Development server or curl for test, if u need test something - write a pytest and execute it using `make test`**

## Implementation Status

| Component | Status |
|-----------|--------|
| Project structure | ✅ Complete |
| Dependencies | ✅ Configured |
| User model | ✅ Created (dataclass + repository) |
| User schemas | ✅ Created (UserCreate, UserResponse) |
| User service | ✅ Created + tests |
| Database config | ✅ Created (SQLite with raw SQL) |
| Main app (FastAPI) | ✅ Created with CORS & lifespan |
| Health endpoint | ✅ Complete (`GET /health`) |
| API documentation | ✅ Complete (`docs/models.md`, `docs/routes.md`) |
| User routes | ⏳ In Progress |
| File storage endpoints | ⏳ Pending |
| Shared storage endpoints | ⏳ Pending |

## Qwen Added Memories
- /Users/loki/llm/fastapi.md
- docs/models.md
- docs/routes.md
