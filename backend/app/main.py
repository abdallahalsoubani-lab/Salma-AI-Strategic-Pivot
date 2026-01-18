from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.api.routes import auth, gateway, api_keys
from app.core.config import settings
from app.db.session import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Salma AI Gateway...")
    yield
    # Shutdown
    print("Shutting down Salma AI Gateway...")

app = FastAPI(
    title="Salma AI Gateway",
    description="Authentication and AI Provider Gateway API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(api_keys.router, prefix="/api/keys", tags=["API Keys"])
app.include_router(gateway.router, prefix="/api/gateway", tags=["Gateway"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "salma-gateway"}

@app.get("/")
async def root():
    return {"message": "Salma AI Gateway API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
