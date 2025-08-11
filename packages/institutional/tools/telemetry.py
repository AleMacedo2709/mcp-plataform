from starlette.middleware.base import BaseHTTPMiddleware
import uuid, time

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        rid = request.headers.get('x-request-id') or str(uuid.uuid4())
        start = time.time()
        response = await call_next(request)
        dur = int((time.time()-start)*1000)
        response.headers['x-request-id'] = rid
        response.headers['x-response-time-ms'] = str(dur)
        return response
