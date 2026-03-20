# Local File Storage System

A FastAPI-based local file storage system that allows user management, per-user file storage, and network-shared storage access without password authentication.

## Features

- **User Management**: Create, list, and delete users
- **Per-User File Storage**: Each user has isolated storage for their files
- **Shared Storage**: Public folder accessible without authentication
- **Network Sharing**: CORS configured for local network access
- **Logging**: Comprehensive logging to file and console
- **Raw SQL**: Uses raw SQLite queries (no ORM)
- **Repository Pattern**: Clean architecture with repository pattern

## Requirements

- Python 3.10+

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd some_project
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment (if not already created)
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Using uv (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

### 4. Configure Environment (Optional)

Copy the example environment file and adjust as needed:

```bash
cp .env.example .env
```

Available environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) | `INFO` |
| `ALLOWED_HOSTS` | CORS allowed hosts (comma-separated) | `*` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

## Running the Server

### Development Mode

```bash
# Activate virtual environment
source .venv/bin/activate

# Run with uvicorn
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

```bash
# Activate virtual environment
source .venv/bin/activate

# Run with uvicorn (without auto-reload)
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The server will be available at:
- **Local**: `http://localhost:8000`
- **Network**: `http://<your-ip>:8000`

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Endpoints

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

## API Usage Examples

### Create a User

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "alice"}'
```

Response:
```json
{
  "id": 1,
  "username": "alice",
  "created_at": "2024-01-01T12:00:00"
}
```

### List All Users

```bash
curl http://localhost:8000/users
```

### Upload a File

```bash
curl -X POST http://localhost:8000/users/1/files \
  -F "file=@/path/to/your/file.txt"
```

Response:
```json
{
  "message": "File uploaded successfully",
  "filename": "file.txt",
  "user_id": 1
}
```

### List User's Files

```bash
curl http://localhost:8000/users/1/files
```

Response:
```json
[
  {
    "id": 1,
    "user_id": 1,
    "filename": "file.txt",
    "created_at": "2024-01-01T12:00:00"
  }
]
```

### Download a File

```bash
# Get file info
curl http://localhost:8000/users/1/files/file.txt

# Download file content
curl -O http://localhost:8000/users/1/files/file.txt/download
```

### Delete a File

```bash
curl -X DELETE http://localhost:8000/users/1/files/file.txt
```

Response:
```json
{
  "message": "File 'file.txt' deleted successfully"
}
```

### Upload to Shared Storage

```bash
curl -X POST http://localhost:8000/shared/files \
  -F "file=@/path/to/your/file.txt"
```

### List Shared Files

```bash
curl http://localhost:8000/shared/files
```

### Download from Shared Storage

```bash
curl -O http://localhost:8000/shared/files/file.txt/download
```

### Delete from Shared Storage

```bash
curl -X DELETE http://localhost:8000/shared/files/file.txt
```

## Testing

Run all tests:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run pytest
uv run pytest
```

Run tests with verbose output:

```bash
uv run pytest -v
```

Run tests with coverage:

```bash
uv run pytest --cov=app
```

## Logging

The application logs to both console and file:

- **Console**: Standard output
- **File**: `logs/app.log`

Log levels available:
- `DEBUG`: Detailed debugging information
- `INFO`: General operational messages
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical errors

Set the log level via environment variable:

```bash
export LOG_LEVEL=DEBUG
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Network Access

To access the server from other devices on your local network:

### 1. Find Your Local IP Address

**macOS:**
```bash
ipconfig getifaddr en0
```

**Linux:**
```bash
hostname -I
```

**Windows:**
```bash
ipconfig
```

### 2. Access from Other Devices

Once you have your IP address (e.g., `192.168.1.100`), other devices can access:

```
http://192.168.1.100:8000
```

### 3. CORS Configuration

By default, CORS is configured to allow all hosts (`*`). For production, restrict this in your `.env` file:

```
ALLOWED_HOSTS=http://localhost:3000,http://example.com
```

## Project Structure

```
some_project/
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI app entry point
│   ├── config.py           # Configuration settings
│   ├── database.py         # Database setup (raw SQL)
│   ├── logging_config.py   # Logging configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py         # User model
│   │   ├── file.py         # File model
│   │   └── shared_file.py  # Shared file model
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
│   │   ├── file_service.py
│   │   └── shared_file_service.py
│   ├── storage/
│   │   ├── database.db     # SQLite database
│   │   ├── users/          # Per-user file storage
│   │   └── shared/         # Shared storage folder
│   └── logs/
│       └── app.log         # Application logs
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_users.py
│   ├── test_files.py
│   └── test_shared.py
├── .env.example            # Example environment file
├── pyproject.toml
├── README.md
└── PLAN.md
```

## Architecture

### Repository Pattern

The application uses the repository pattern for data access:

```
Router → Service → Repository → Database
```

- **Routers**: Handle HTTP requests/responses
- **Services**: Business logic layer
- **Repositories**: Data access layer with raw SQL
- **Database**: SQLite for persistence

### No ORM

The application uses raw SQL queries instead of an ORM (like SQLAlchemy) for:
- Direct control over SQL queries
- Better performance for simple operations
- No additional dependencies
- Transparent database operations

## Troubleshooting

### Database Issues

If you encounter database errors, try removing and recreating the database:

```bash
rm app/storage/database.db
# Restart the server - database will be recreated automatically
```

### Permission Issues

Ensure the application has write permissions to the storage directory:

```bash
chmod -R 755 app/storage
```

### Port Already in Use

If port 8000 is already in use, specify a different port:

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8001
```

## License

MIT
