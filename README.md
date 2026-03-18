# Local File Storage System

A FastAPI-based local file storage system that allows user management, per-user file storage, and network-shared storage access without password authentication.

## Features

- **User Management**: Create, list, and delete users
- **Per-User File Storage**: Each user has isolated storage for their files
- **Shared Storage**: Public folder accessible without authentication
- **Network Sharing**: CORS configured for local network access

## Requirements

- Python 3.10+

## Installation

```bash
source .venv/bin/activate
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The server will be available at:
- Local: `http://localhost:8000`
- Network: `http://<your-ip>:8000`

## API Documentation

Once the server is running, access the interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |

### Users (Coming Soon)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users` | Create a new user |
| GET | `/users` | List all users |
| GET | `/users/{user_id}` | Get user details |
| DELETE | `/users/{user_id}` | Delete a user |

### User Files (Coming Soon)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/{user_id}/files` | Upload a file |
| GET | `/users/{user_id}/files` | List user's files |
| GET | `/users/{user_id}/files/{filename}` | Download a file |
| DELETE | `/users/{user_id}/files/{filename}` | Delete a file |

### Shared Storage (Coming Soon)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/shared/files` | Upload to shared storage |
| GET | `/shared/files` | List shared files |
| GET | `/shared/files/{filename}` | Download from shared |
| DELETE | `/shared/files/{filename}` | Delete shared file |

## Testing

```bash
uv run pytest
```

## Project Structure

```
some_project/
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI app entry point
│   ├── config.py           # Configuration settings
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   ├── routers/            # API routers
│   ├── services/           # Business logic
│   └── storage/            # File storage location
│       ├── users/          # Per-user folders
│       └── shared/         # Shared storage folder
├── tests/
├── pyproject.toml
└── README.md
```

## Network Access

To access the server from other devices on your local network:

1. Find your local IP address:
   - macOS: `ipconfig getifaddr en0`
   - Linux: `hostname -I`
   - Windows: `ipconfig`

2. Access from other devices: `http://<your-ip>:8000`

## License

MIT
