from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4
from datetime import datetime
from app.connectors.data.base import ConnectionConfig, ConnectionType, DataConnectorBase, QueryResult
from app.connectors.data.postgresql import PostgreSQLConnector
from app.connectors.data.mysql import MySQLConnector
from app.connectors.data.oracle import OracleConnector
from app.connectors.data.rest_api import RestAPIConnector


class ConnectionService:
    """Manages data source connections"""

    CONNECTOR_MAP = {
        ConnectionType.POSTGRESQL: PostgreSQLConnector,
        ConnectionType.MYSQL: MySQLConnector,
        ConnectionType.ORACLE: OracleConnector,
        ConnectionType.REST_API: RestAPIConnector,
    }

    def __init__(self):
        # Active connection instances: {connection_id: connector_instance}
        self._connections: Dict[UUID, DataConnectorBase] = {}
        # Connection metadata: {connection_id: {name, type, created_at, ...}}
        self._connection_metadata: Dict[UUID, Dict[str, Any]] = {}

    def get_connector_class(self, conn_type: ConnectionType) -> type:
        """Get connector class for connection type"""
        connector_class = self.CONNECTOR_MAP.get(conn_type)
        if not connector_class:
            raise ValueError(f"Unsupported connection type: {conn_type}")
        return connector_class

    async def test_connection(
        self,
        conn_type: ConnectionType,
        config: ConnectionConfig
    ) -> Dict[str, Any]:
        """Test a connection without saving"""
        connector_class = self.get_connector_class(conn_type)
        connector = connector_class()
        return await connector.test_connection(config)

    async def create_connection(
        self,
        user_id: UUID,
        name: str,
        conn_type: ConnectionType,
        config: ConnectionConfig
    ) -> Dict[str, Any]:
        """Create and establish a connection"""

        # Test connection first
        test_result = await self.test_connection(conn_type, config)
        if not test_result["success"]:
            return {
                "success": False,
                "message": test_result["message"],
                "error": test_result.get("error")
            }

        # Create connector instance
        connector_class = self.get_connector_class(conn_type)
        connector = connector_class()

        try:
            # Connect
            await connector.connect(config)

            # Generate connection ID
            connection_id = uuid4()

            # Store connection
            self._connections[connection_id] = connector
            self._connection_metadata[connection_id] = {
                "name": name,
                "type": conn_type,
                "user_id": user_id,
                "created_at": datetime.utcnow(),
                "last_used": None,
                "host": config.host,
                "database": config.database
            }

            return {
                "success": True,
                "message": "تم إنشاء الاتصال بنجاح",
                "connection_id": str(connection_id)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"فشل إنشاء الاتصال: {str(e)}",
                "error": str(e)
            }

    async def get_connection(self, connection_id: UUID) -> Optional[DataConnectorBase]:
        """Get an active connection instance"""
        return self._connections.get(connection_id)

    async def execute_query_on_connection(
        self,
        connection_id: UUID,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> QueryResult:
        """Execute query on a specific connection"""
        connector = await self.get_connection(connection_id)
        if not connector:
            raise ConnectionError("Connection not found or not active")

        # Update last used timestamp
        if connection_id in self._connection_metadata:
            self._connection_metadata[connection_id]["last_used"] = datetime.utcnow()

        return await connector.execute_query(query, params)

    async def get_connection_schema(self, connection_id: UUID) -> Dict[str, Any]:
        """Get schema for a connection"""
        connector = await self.get_connection(connection_id)
        if not connector:
            raise ConnectionError("Connection not found")

        return await connector.get_schema()

    async def close_connection(self, connection_id: UUID) -> None:
        """Close a specific connection"""
        if connection_id in self._connections:
            try:
                await self._connections[connection_id].disconnect()
            except Exception as e:
                print(f"Error disconnecting: {str(e)}")
            finally:
                del self._connections[connection_id]
                if connection_id in self._connection_metadata:
                    del self._connection_metadata[connection_id]

    def get_available_connectors(self) -> List[Dict[str, Any]]:
        """Get list of available connector types"""
        return [
            {
                "type": ConnectionType.POSTGRESQL.value,
                "name": "PostgreSQL",
                "name_ar": "بوستجريس كيو إل",
                "icon": "postgresql",
                "default_port": 5432
            },
            {
                "type": ConnectionType.MYSQL.value,
                "name": "MySQL",
                "name_ar": "ماي إس كيو إل",
                "icon": "mysql",
                "default_port": 3306
            },
            {
                "type": ConnectionType.ORACLE.value,
                "name": "Oracle Database",
                "name_ar": "قاعدة بيانات أوراكل",
                "icon": "oracle",
                "default_port": 1521
            },
            {
                "type": ConnectionType.REST_API.value,
                "name": "REST API",
                "name_ar": "واجهة برمجة REST",
                "icon": "api",
                "default_port": None
            }
        ]

    def get_user_connections(self, user_id: UUID) -> List[Dict[str, Any]]:
        """Get all connections for a user"""
        user_connections = []
        for conn_id, metadata in self._connection_metadata.items():
            if metadata.get("user_id") == user_id:
                user_connections.append({
                    "id": str(conn_id),
                    **metadata,
                    "created_at": metadata["created_at"].isoformat(),
                    "last_used": metadata["last_used"].isoformat() if metadata["last_used"] else None
                })
        return user_connections

    def get_connection_metadata(self, connection_id: UUID) -> Optional[Dict[str, Any]]:
        """Get metadata for a connection"""
        metadata = self._connection_metadata.get(connection_id)
        if metadata:
            return {
                **metadata,
                "created_at": metadata["created_at"].isoformat(),
                "last_used": metadata["last_used"].isoformat() if metadata["last_used"] else None
            }
        return None


# Global instance
connection_service = ConnectionService()
