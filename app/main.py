from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOWED_HOSTS, LOG_LEVEL
from app.database import init_db
from app.logging_config import setup_logging
from app.routers.files import router as files_router
from app.routers.shared import router as shared_router
from app.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Setup logging
    setup_logging(LOG_LEVEL)
    
    # Initialize database
    init_db()
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title="Local File Storage System",
    description="A FastAPI-based local file storage system with user management and shared storage",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS for local network access
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(users_router)
app.include_router(files_router)
app.include_router(shared_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint to verify the service is running."""
    return {"status": "healthy"}
