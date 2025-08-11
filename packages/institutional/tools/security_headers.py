from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.responses import Response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, csp: str | None = None):
        super().__init__(app)
        self.csp = csp or "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self' *; frame-ancestors 'none'"
    async def dispatch(self, request, call_next):
        resp: Response = await call_next(request)
        resp.headers['Content-Security-Policy'] = self.csp
        resp.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
        resp.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
        resp.headers['Cross-Origin-Resource-Policy'] = 'same-site'
        resp.headers['X-Content-Type-Options'] = 'nosniff'
        resp.headers['X-Frame-Options'] = 'DENY'
        resp.headers['Referrer-Policy'] = 'no-referrer'
        return resp
