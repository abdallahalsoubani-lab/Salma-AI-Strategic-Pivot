"""
تطبيق Salma AI Gateway
Salma AI Gateway - Main Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.database import init_db, close_db
from app.api.routes import audit

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events"""
    # Startup
    logger.info("Starting Salma AI Gateway...")
    await init_db()
    logger.info("Database initialized")

    yield

    # Shutdown
    logger.info("Shutting down Salma AI Gateway...")
    await close_db()


# Create FastAPI app
app = FastAPI(
    title="Salma AI Gateway",
    description="الدرع الموحد للذكاء الاصطناعي - Unified AI Shield",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(audit.router)


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Salma AI Gateway",
        "version": "1.0.0"
    }


@app.get("/api/health")
async def api_health():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "api": "Audit & XAI",
        "timestamp": None
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
