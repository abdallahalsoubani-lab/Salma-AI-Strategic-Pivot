import httpx
import base64
from typing import List, Dict, Any, Optional
from datetime import datetime
from .base import DataConnectorBase, ConnectionConfig, ConnectionType, QueryResult


class RestAPIConnector(DataConnectorBase):
    """Generic REST API Connector"""

    connector_type = ConnectionType.REST_API
    connector_name = "REST API"
    connector_name_ar = "واجهة برمجة REST"

    def __init__(self):
        self.client = None
        self.config = None
        self.base_url = None

    async def connect(self, config: ConnectionConfig) -> bool:
        """Initialize HTTP client"""
        try:
            self.config = config
            self.base_url = config.host.rstrip('/') if config.host else ""

            headers = {}

            # Handle authentication
            auth_config = config.additional_config or {}
            auth_type = auth_config.get("auth_type", "none")

            if auth_type == "bearer":
                headers["Authorization"] = f"Bearer {auth_config.get('token')}"
            elif auth_type == "api_key":
                key_name = auth_config.get("api_key_header", "X-API-Key")
                headers[key_name] = auth_config.get("api_key")
            elif auth_type == "basic":
                credentials = base64.b64encode(
                    f"{config.username}:{config.password}".encode()
                ).decode()
                headers["Authorization"] = f"Basic {credentials}"

            # Add custom headers
            custom_headers = auth_config.get("headers", {})
            headers.update(custom_headers)

            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=headers,
                timeout=30.0
            )

            return True
        except Exception as e:
            raise ConnectionError(f"Failed to initialize: {str(e)}")

    async def disconnect(self) -> None:
        """Close HTTP client"""
        if self.client:
            await self.client.aclose()
            self.client = None

    async def test_connection(self, config: ConnectionConfig) -> Dict[str, Any]:
        """Test API connection"""
        try:
            await self.connect(config)

            # Try to hit the base URL or a health endpoint
            test_endpoint = (config.additional_config or {}).get("test_endpoint", "/")
            response = await self.client.get(test_endpoint)

            await self.disconnect()

            return {
                "success": response.status_code < 400,
                "message": "تم الاتصال بنجاح" if response.status_code < 400 else "فشل الاتصال",
                "status_code": response.status_code,
                "base_url": config.host
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
        """
        Execute API request
        Query format: "METHOD /endpoint" e.g., "GET /users" or "POST /data"
        """
        if not self.client:
            raise ConnectionError("Not connected")

        start_time = datetime.utcnow()

        # Parse query
        parts = query.strip().split(" ", 1)
        method = parts[0].upper() if len(parts) > 0 else "GET"
        endpoint = parts[1] if len(parts) > 1 else "/"

        # Add limit to params if GET request
        request_params = params or {}
        if method == "GET" and "limit" not in request_params:
            request_params["limit"] = limit

        # Execute request
        try:
            if method == "GET":
                response = await self.client.get(endpoint, params=request_params)
            elif method == "POST":
                response = await self.client.post(endpoint, json=request_params)
            elif method == "PUT":
                response = await self.client.put(endpoint, json=request_params)
            elif method == "DELETE":
                response = await self.client.delete(endpoint, params=request_params)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError as e:
            raise ValueError(f"HTTP Error: {str(e)}")

        execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)

        # Convert response to table format
        if isinstance(data, list):
            rows = data[:limit]
            columns = list(rows[0].keys()) if rows else []
            table_rows = [[row.get(col) for col in columns] for row in rows]
        elif isinstance(data, dict):
            # Check if response has a data/items/results array
            found = False
            for key in ["data", "items", "results", "records"]:
                if key in data and isinstance(data[key], list):
                    rows = data[key][:limit]
                    columns = list(rows[0].keys()) if rows else []
                    table_rows = [[row.get(col) for col in columns] for row in rows]
                    found = True
                    break
            if not found:
                # Single object response
                columns = list(data.keys())
                table_rows = [[data.get(col) for col in columns]]
        else:
            columns = ["response"]
            table_rows = [[str(data)]]

        return QueryResult(
            columns=columns,
            rows=table_rows,
            row_count=len(table_rows),
            execution_time_ms=execution_time,
            truncated=len(table_rows) >= limit
        )

    async def get_schema(self) -> Dict[str, Any]:
        """REST APIs don't have traditional schemas"""
        return {
            "type": "rest_api",
            "base_url": self.base_url,
            "message": "REST API - no schema available"
        }

    async def get_tables(self) -> List[str]:
        """Return configured endpoints as 'tables'"""
        endpoints = (self.config.additional_config or {}).get("endpoints", [])
        return endpoints if endpoints else ["/"]

    async def get_table_columns(self, table_name: str) -> List[Dict[str, str]]:
        """Try to infer columns from a sample request"""
        try:
            result = await self.execute_query(f"GET {table_name}", limit=1)
            return [{"name": col, "type": "dynamic"} for col in result.columns]
        except:
            return []

    async def get_sample_data(self, table_name: str, limit: int = 10) -> QueryResult:
        return await self.execute_query(f"GET {table_name}", limit=limit)
