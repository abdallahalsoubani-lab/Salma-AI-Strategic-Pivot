import aiomysql
from typing import List, Dict, Any, Optional
from datetime import datetime
from .base import DataConnectorBase, ConnectionConfig, ConnectionType, QueryResult


class MySQLConnector(DataConnectorBase):
    """MySQL Database Connector"""

    connector_type = ConnectionType.MYSQL
    connector_name = "MySQL"
    connector_name_ar = "ماي إس كيو إل"

    def __init__(self):
        self.pool = None
        self.config = None

    async def connect(self, config: ConnectionConfig) -> bool:
        """Create connection pool"""
        try:
            self.config = config
            self.pool = await aiomysql.create_pool(
                host=config.host,
                port=config.port or 3306,
                db=config.database,
                user=config.username,
                password=config.password,
                minsize=1,
                maxsize=10,
                connect_timeout=10
            )
            return True
        except Exception as e:
            raise ConnectionError(f"Failed to connect: {str(e)}")

    async def disconnect(self) -> None:
        """Close connection pool"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None

    async def test_connection(self, config: ConnectionConfig) -> Dict[str, Any]:
        """Test connection"""
        try:
            conn = await aiomysql.connect(
                host=config.host,
                port=config.port or 3306,
                db=config.database,
                user=config.username,
                password=config.password,
                connect_timeout=10
            )

            async with conn.cursor() as cursor:
                await cursor.execute("SELECT VERSION()")
                version = await cursor.fetchone()

            conn.close()

            return {
                "success": True,
                "message": "تم الاتصال بنجاح",
                "server_version": version[0],
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

        query_upper = query.strip().upper()
        if query_upper.startswith("SELECT") and "LIMIT" not in query_upper:
            query = f"{query.rstrip(';')} LIMIT {limit}"

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                if params:
                    await cursor.execute(query, tuple(params.values()))
                else:
                    await cursor.execute(query)

                rows = await cursor.fetchall()
                columns = [desc[0] for desc in cursor.description] if cursor.description else []

        execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)

        return QueryResult(
            columns=columns,
            rows=[list(row) for row in rows],
            row_count=len(rows),
            execution_time_ms=execution_time,
            truncated=len(rows) >= limit
        )

    async def get_schema(self) -> Dict[str, Any]:
        tables = await self.get_tables()
        schema = {}
        for table in tables:
            columns = await self.get_table_columns(table)
            schema[table] = columns
        return schema

    async def get_tables(self) -> List[str]:
        query = "SHOW TABLES"
        result = await self.execute_query(query)
        return [row[0] for row in result.rows]

    async def get_table_columns(self, table_name: str) -> List[Dict[str, str]]:
        query = f"DESCRIBE `{table_name}`"
        result = await self.execute_query(query)
        return [
            {
                "name": row[0],
                "type": row[1],
                "nullable": row[2] == "YES",
                "default": row[4]
            }
            for row in result.rows
        ]

    async def get_sample_data(self, table_name: str, limit: int = 10) -> QueryResult:
        safe_table = table_name.replace('`', '``')
        query = f"SELECT * FROM `{safe_table}` LIMIT {limit}"
        return await self.execute_query(query)
