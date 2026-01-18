"""
مقاييس Prometheus
Prometheus Metrics for monitoring
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import time


# Request metrics
REQUEST_COUNT = Counter(
    'salma_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'salma_http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# AI Gateway metrics
AI_REQUESTS = Counter(
    'salma_ai_requests_total',
    'Total AI requests',
    ['provider', 'model', 'status']
)

AI_LATENCY = Histogram(
    'salma_ai_request_duration_seconds',
    'AI request latency',
    ['provider', 'model'],
    buckets=[0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0]
)

AI_TOKENS = Counter(
    'salma_ai_tokens_total',
    'Total AI tokens used',
    ['provider', 'model', 'type']  # type: input/output
)

AI_COST = Counter(
    'salma_ai_cost_usd_total',
    'Total AI cost in USD',
    ['provider', 'model']
)

# Document processing metrics
DOCUMENTS_PROCESSED = Counter(
    'salma_documents_processed_total',
    'Total documents processed',
    ['type', 'status']
)

DOCUMENT_PROCESSING_TIME = Histogram(
    'salma_document_processing_seconds',
    'Document processing time',
    ['type'],
    buckets=[1.0, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0]
)

# Active connections
ACTIVE_CONNECTIONS = Gauge(
    'salma_active_connections',
    'Number of active data source connections',
    ['type']
)

ACTIVE_USERS = Gauge(
    'salma_active_users',
    'Number of active users (last 5 minutes)'
)


def get_metrics():
    """Get Prometheus metrics"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


class MetricsMiddleware:
    """Middleware to collect request metrics"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)

        start_time = time.time()

        # Get request info
        method = scope['method']
        path = scope['path']

        # Process request
        status_code = 500

        async def send_wrapper(message):
            nonlocal status_code
            if message['type'] == 'http.response.start':
                status_code = message['status']
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            # Record metrics
            duration = time.time() - start_time

            # Normalize path for metrics (remove IDs)
            normalized_path = self._normalize_path(path)

            REQUEST_COUNT.labels(
                method=method,
                endpoint=normalized_path,
                status=status_code
            ).inc()

            REQUEST_LATENCY.labels(
                method=method,
                endpoint=normalized_path
            ).observe(duration)

    def _normalize_path(self, path: str) -> str:
        """Normalize path for metrics (replace IDs with placeholders)"""
        import re
        # Replace UUIDs
        path = re.sub(
            r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
            '{id}',
            path
        )
        # Replace numeric IDs
        path = re.sub(r'/\d+', '/{id}', path)
        return path
