from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from config import settings
import logging

logger = logging.getLogger(__name__)


async def api_key_auth_middleware(request: Request, call_next):
    """Middleware to authenticate requests using API key."""
    # Skip authentication for health check and docs
    if request.url.path in ["/", "/docs", "/redoc", "/openapi.json"]:
        return await call_next(request)

    # Check for API key in header
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != settings.api_key:
        logger.warning(f"Unauthorized access attempt from {request.client.host}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid or missing API key"}
        )

    return await call_next(request)