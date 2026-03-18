from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOWED_HOSTS

app = FastAPI(
    title="Local File Storage System",
    description="A FastAPI-based local file storage system with user management and shared storage",
    version="0.1.0",
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
def health_check():
    """Health check endpoint to verify the service is running."""
    return {"status": "healthy"}
