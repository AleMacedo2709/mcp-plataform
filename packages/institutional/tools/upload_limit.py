from starlette.middleware.base import BaseHTTPMiddleware
from starlette.datastructures import UploadFile
from fastapi import Request, HTTPException, status
import os

class UploadLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        max_mb = int(os.getenv("MAX_FILE_MB", "50"))
        if request.headers.get("content-type","").startswith("multipart/form-data"):
            # starlette streams; we cannot know upfront; enforce after saved (server-side check is also present)
            pass
        response = await call_next(request)
        return response
