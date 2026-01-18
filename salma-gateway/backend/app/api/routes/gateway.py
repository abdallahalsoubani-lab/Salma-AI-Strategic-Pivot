"""Gateway routes (placeholder)"""
from fastapi import APIRouter

router = APIRouter(prefix="/gateway", tags=["gateway"])


@router.post("/query")
async def query() -> dict:
    """Query gateway endpoint - placeholder"""
    return {"message": "Query endpoint - implementation pending"}


@router.get("/connections")
async def list_connections() -> dict:
    """List connections endpoint - placeholder"""
    return {"message": "List connections endpoint - implementation pending"}


@router.post("/connections")
async def create_connection() -> dict:
    """Create connection endpoint - placeholder"""
    return {"message": "Create connection endpoint - implementation pending"}
