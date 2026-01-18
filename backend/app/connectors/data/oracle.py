import oracledb
from typing import List, Dict, Any, Optional
from datetime import datetime
from .base import DataConnectorBase, ConnectionConfig, ConnectionType, QueryResult


class OracleConnector(DataConnectorBase):
    """Oracle Database Connector"""

    connector_type = ConnectionType.ORACLE
    connector_name = "Oracle Database"
    connector_name_ar = "قاعدة بيانات أوراكل"

    def __init__(self):
        self.pool = None
        self.config = None
        # Enable thin mode (no Oracle Client needed)
        try:
            oracledb.init_oracle_client()
        except:
            # Thin mode - no need to initialize
            pass

    async def connect(self, config: ConnectionConfig) -> bool:
        """Create connection pool"""
        try:
            self.config = config

            # Build DSN
            dsn = f"{config.host}:{config.port or 1521}/{config.database}"

            self.pool = oracledb.create_pool(
                user=config.username,
                password=config.password,
                dsn=dsn,
                min=1,
                max=10,
                increment=1
            )
            return True
        except Exception as e:
            raise ConnectionError(f"Failed to connect: {str(e)}")

    async def disconnect(self) -> None:
        """Close connection pool"""
        if self.pool:
            self.pool.close()
            self.pool = None

    async def test_connection(self, config: ConnectionConfig) -> Dict[str, Any]:
        """Test connection"""
        try:
            dsn = f"{config.host}:{config.port or 1521}/{config.database}"

            conn = oracledb.connect(
                user=config.username,
                password=config.password,
                dsn=dsn
            )

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM V$VERSION WHERE ROWNUM = 1")
            version = cursor.fetchone()

            cursor.close()
            conn.close()

            return {
                "success": True,
                "message": "تم الاتصال بنجاح",
                "server_version": version[0] if version else "Unknown",
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

        # Oracle uses FETCH FIRST for limiting
        query_upper = query.strip().upper()
        if query_upper.startswith("SELECT") and "FETCH" not in query_upper and "ROWNUM" not in query_upper:
            query = f"{query.rstrip(';')} FETCH FIRST {limit} ROWS ONLY"

        conn = self.pool.acquire()
        cursor = conn.cursor()

        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []

            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)

            return QueryResult(
                columns=columns,
                rows=[list(row) for row in rows],
                row_count=len(rows),
                execution_time_ms=execution_time,
                truncated=len(rows) >= limit
            )
        finally:
            cursor.close()
            self.pool.release(conn)

    async def get_schema(self) -> Dict[str, Any]:
        tables = await self.get_tables()
        schema = {}
        for table in tables:
            columns = await self.get_table_columns(table)
            schema[table] = columns
        return schema

    async def get_tables(self) -> List[str]:
        query = """
            SELECT table_name
            FROM user_tables
            ORDER BY table_name
        """
        result = await self.execute_query(query)
        return [row[0] for row in result.rows]

    async def get_table_columns(self, table_name: str) -> List[Dict[str, str]]:
        query = """
            SELECT column_name, data_type, nullable, data_default
            FROM user_tab_columns
            WHERE table_name = :table_name
            ORDER BY column_id
        """
        result = await self.execute_query(query, {"table_name": table_name.upper()})
        return [
            {
                "name": row[0],
                "type": row[1],
                "nullable": row[2] == "Y",
                "default": row[3]
            }
            for row in result.rows
        ]

    async def get_sample_data(self, table_name: str, limit: int = 10) -> QueryResult:
        safe_table = table_name.replace('"', '""')
        query = f'SELECT * FROM "{safe_table}" FETCH FIRST {limit} ROWS ONLY'
        return await self.execute_query(query)
