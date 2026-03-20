# Project Context: some_project

## Project Overview

This is a **FastAPI (Python)** project that implements a **local file storage system** designed to be shared across a local network.

### Key Features
- User creation and management
- File storage per user
- Network-shared storage access
- Password-free access for shared storage

## Current State

**✅ Project Initialized**

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
│   ├── database.py          # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # User model
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
├── tests/
│   ├── __init__.py
│   └── test_user_service.py # User service tests
├── pyproject.toml
├── README.md
└── QWEN.md
```

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

## Implementation Status

| Component | Status |
|-----------|--------|
| Project structure | ✅ Complete |
| Dependencies | ✅ Configured |
| User model | ✅ Created |
| User schemas | ✅ Created |
| User service | ✅ Created + tests |
| Database config | ✅ Created |
| Main app (FastAPI) | ✅ Created with CORS & lifespan |
| API routers | ⏳ Pending |
| File storage endpoints | ⏳ Pending |
| Shared storage endpoints | ⏳ Pending |

## Qwen Added Memories
- /Users/loki/llm/fastapi.md
