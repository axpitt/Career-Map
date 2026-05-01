from slowapi import Limiter
from slowapi.util import get_remote_address
from config import settings

# Rate limiter instance
limiter = Limiter(key_func=get_remote_address)

# Rate limit string for analyze endpoint
ANALYZE_RATE_LIMIT = f"{settings.rate_limit_requests} per {settings.rate_limit_window} seconds"