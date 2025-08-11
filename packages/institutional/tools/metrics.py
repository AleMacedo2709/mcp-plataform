from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['service','method','path','status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency', ['service','method','path'])

class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, service: str):
        super().__init__(app)
        self.service = service
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        dur = time.perf_counter() - start
        REQUEST_COUNT.labels(self.service, request.method, request.url.path, str(response.status_code)).inc()
        REQUEST_LATENCY.labels(self.service, request.method, request.url.path).observe(dur)
        return response

def metrics_endpoint():
    def _metrics():
        data = generate_latest()
        return Response(content=data, media_type=CONTENT_TYPE_LATEST)
    return _metrics
