from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOWED_HOSTS
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup: initialize database
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


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint to verify the service is running."""
    return {"status": "healthy"}
