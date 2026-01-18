from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from enum import Enum


class ConnectionType(str, Enum):
    ORACLE = "oracle"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MSSQL = "mssql"
    REST_API = "rest_api"
    MONGODB = "mongodb"


class ConnectionConfig(BaseModel):
    """Base configuration for data connections"""
    name: str
    type: ConnectionType
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None  # Will be encrypted
    additional_config: Optional[Dict[str, Any]] = None


class QueryResult(BaseModel):
    """Standard query result format"""
    columns: List[str]
    rows: List[List[Any]]
    row_count: int
    execution_time_ms: int
    truncated: bool = False  # True if results were limited


class DataConnectorBase(ABC):
    """Base class for all data source connectors"""

    connector_type: ConnectionType
    connector_name: str
    connector_name_ar: str

    @abstractmethod
    async def connect(self, config: ConnectionConfig) -> bool:
        """Establish connection to data source"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection"""
        pass

    @abstractmethod
    async def test_connection(self, config: ConnectionConfig) -> Dict[str, Any]:
        """Test if connection is valid"""
        pass

    @abstractmethod
    async def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        limit: int = 1000
    ) -> QueryResult:
        """Execute a query and return results"""
        pass

    @abstractmethod
    async def get_schema(self) -> Dict[str, Any]:
        """Get database schema (tables, columns, types)"""
        pass

    @abstractmethod
    async def get_tables(self) -> List[str]:
        """Get list of available tables"""
        pass

    @abstractmethod
    async def get_table_columns(self, table_name: str) -> List[Dict[str, str]]:
        """Get columns for a specific table"""
        pass

    @abstractmethod
    async def get_sample_data(self, table_name: str, limit: int = 10) -> QueryResult:
        """Get sample data from a table"""
        pass
