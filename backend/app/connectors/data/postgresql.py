import asyncpg
from typing import List, Dict, Any, Optional
from datetime import datetime
from .base import DataConnectorBase, ConnectionConfig, ConnectionType, QueryResult


class PostgreSQLConnector(DataConnectorBase):
    """PostgreSQL Database Connector"""

    connector_type = ConnectionType.POSTGRESQL
    connector_name = "PostgreSQL"
    connector_name_ar = "بوستجريس كيو إل"

    def __init__(self):
        self.pool = None
        self.config = None

    async def connect(self, config: ConnectionConfig) -> bool:
        """Create connection pool"""
        try:
            self.config = config
            self.pool = await asyncpg.create_pool(
                host=config.host,
                port=config.port or 5432,
                database=config.database,
                user=config.username,
                password=config.password,
                min_size=1,
                max_size=10,
                command_timeout=60
            )
            return True
        except Exception as e:
            raise ConnectionError(f"Failed to connect: {str(e)}")

    async def disconnect(self) -> None:
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def test_connection(self, config: ConnectionConfig) -> Dict[str, Any]:
        """Test connection and return server info"""
        try:
            conn = await asyncpg.connect(
                host=config.host,
                port=config.port or 5432,
                database=config.database,
                user=config.username,
                password=config.password,
                timeout=10
            )

            version = await conn.fetchval("SELECT version()")
            await conn.close()

            return {
                "success": True,
                "message": "تم الاتصال بنجاح",
                "server_version": version,
                "database": config.database
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"فشل الاتصال: {str(e)}",
                "error": str(e)
            }

    async def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        limit: int = 1000
    ) -> QueryResult:
        """Execute SQL query"""
        if not self.pool:
            raise ConnectionError("Not connected")

        start_time = datetime.utcnow()

        # Add LIMIT if not present and it's a SELECT query
        query_upper = query.strip().upper()
        if query_upper.startswith("SELECT") and "LIMIT" not in query_upper:
            query = f"{query.rstrip(';')} LIMIT {limit}"

        async with self.pool.acquire() as conn:
            # Execute query
            if params:
                rows = await conn.fetch(query, *params.values())
            else:
                rows = await conn.fetch(query)

            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)

            if rows:
                columns = list(rows[0].keys())
                data = [list(row.values()) for row in rows]
            else:
                columns = []
                data = []

            return QueryResult(
                columns=columns,
                rows=data,
                row_count=len(data),
                execution_time_ms=execution_time,
                truncated=len(data) >= limit
            )

    async def get_schema(self) -> Dict[str, Any]:
        """Get full database schema"""
        tables = await self.get_tables()
        schema = {}

        for table in tables:
            columns = await self.get_table_columns(table)
            schema[table] = columns

        return schema

    async def get_tables(self) -> List[str]:
        """Get list of tables"""
        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """
        result = await self.execute_query(query)
        return [row[0] for row in result.rows]

    async def get_table_columns(self, table_name: str) -> List[Dict[str, str]]:
        """Get columns for a table"""
        query = """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = $1
            ORDER BY ordinal_position
        """
        result = await self.execute_query(query, {"table": table_name})

        return [
            {
                "name": row[0],
                "type": row[1],
                "nullable": row[2] == "YES",
                "default": row[3]
            }
            for row in result.rows
        ]

    async def get_sample_data(self, table_name: str, limit: int = 10) -> QueryResult:
        """Get sample data from table"""
        # Sanitize table name to prevent SQL injection
        safe_table = table_name.replace('"', '""')
        query = f'SELECT * FROM "{safe_table}" LIMIT {limit}'
        return await self.execute_query(query)
