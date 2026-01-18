from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from app.services.connection_service import connection_service
from app.connectors.data.base import ConnectionConfig, ConnectionType


router = APIRouter(prefix="/api/connections", tags=["connections"])


# Request Models
class CreateConnectionRequest(BaseModel):
    name: str
    type: ConnectionType
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    additional_config: Optional[dict] = None


class TestConnectionRequest(BaseModel):
    type: ConnectionType
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    additional_config: Optional[dict] = None


class QueryRequest(BaseModel):
    query: str
    params: Optional[dict] = None


# Endpoints
@router.get("/types")
async def get_connection_types():
    """Get available connection types"""
    return {
        "types": connection_service.get_available_connectors()
    }


@router.post("/test")
async def test_connection(request: TestConnectionRequest):
    """Test a connection without saving"""
    config = ConnectionConfig(
        name="test",
        type=request.type,
        host=request.host,
        port=request.port,
        database=request.database,
        username=request.username,
        password=request.password,
        additional_config=request.additional_config
    )

    result = await connection_service.test_connection(request.type, config)
    return result


@router.post("")
async def create_connection(request: CreateConnectionRequest):
    """Create a new data source connection"""
    config = ConnectionConfig(
        name=request.name,
        type=request.type,
        host=request.host,
        port=request.port,
        database=request.database,
        username=request.username,
        password=request.password,
        additional_config=request.additional_config
    )

    # For now, use a dummy user_id. This should come from authentication in production
    from uuid import uuid4
    user_id = uuid4()

    result = await connection_service.create_connection(
        user_id=user_id,
        name=request.name,
        conn_type=request.type,
        config=config
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return result


@router.get("")
async def list_connections():
    """List all active connections"""
    # For now, use a dummy user_id
    from uuid import uuid4
    user_id = uuid4()

    connections = connection_service.get_user_connections(user_id)
    return {"connections": connections}


@router.get("/{connection_id}")
async def get_connection(connection_id: str):
    """Get connection details"""
    try:
        conn_uuid = UUID(connection_id)
        metadata = connection_service.get_connection_metadata(conn_uuid)
        if not metadata:
            raise HTTPException(status_code=404, detail="Connection not found")
        return metadata
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid connection ID")


@router.delete("/{connection_id}")
async def delete_connection(connection_id: str):
    """Delete a connection"""
    try:
        conn_uuid = UUID(connection_id)
        await connection_service.close_connection(conn_uuid)
        return {"message": "تم حذف الاتصال بنجاح"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid connection ID")


@router.get("/{connection_id}/schema")
async def get_connection_schema(connection_id: str):
    """Get schema for a connection"""
    try:
        conn_uuid = UUID(connection_id)
        connector = await connection_service.get_connection(conn_uuid)
        if not connector:
            raise HTTPException(status_code=404, detail="Connection not found")

        schema = await connector.get_schema()
        return {"schema": schema}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid connection ID")


@router.get("/{connection_id}/tables")
async def get_connection_tables(connection_id: str):
    """Get tables for a connection"""
    try:
        conn_uuid = UUID(connection_id)
        connector = await connection_service.get_connection(conn_uuid)
        if not connector:
            raise HTTPException(status_code=404, detail="Connection not found")

        tables = await connector.get_tables()
        return {"tables": tables}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid connection ID")


@router.get("/{connection_id}/tables/{table_name}/columns")
async def get_table_columns(connection_id: str, table_name: str):
    """Get columns for a table"""
    try:
        conn_uuid = UUID(connection_id)
        connector = await connection_service.get_connection(conn_uuid)
        if not connector:
            raise HTTPException(status_code=404, detail="Connection not found")

        columns = await connector.get_table_columns(table_name)
        return {"columns": columns}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid connection ID")


@router.get("/{connection_id}/tables/{table_name}/sample")
async def get_table_sample(
    connection_id: str,
    table_name: str,
    limit: int = Query(10, ge=1, le=1000)
):
    """Get sample data from a table"""
    try:
        conn_uuid = UUID(connection_id)
        connector = await connection_service.get_connection(conn_uuid)
        if not connector:
            raise HTTPException(status_code=404, detail="Connection not found")

        result = await connector.get_sample_data(table_name, limit)
        return result.model_dump()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid connection ID")


@router.post("/{connection_id}/query")
async def execute_query(
    connection_id: str,
    request: QueryRequest
):
    """Execute a query on a connection"""
    try:
        conn_uuid = UUID(connection_id)
        result = await connection_service.execute_query_on_connection(
            conn_uuid,
            request.query,
            request.params
        )
        return result.model_dump()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid connection ID")
    except ConnectionError as e:
        raise HTTPException(status_code=404, detail=str(e))
