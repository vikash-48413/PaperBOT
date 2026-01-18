"""
Simple rate limiter for API endpoints.
Prevents abuse and protects external API quotas.
"""

import time
from collections import defaultdict
from functools import wraps
from fastapi import HTTPException, Request
from typing import Dict, Tuple

class RateLimiter:
    """
    Token bucket rate limiter.
    Allows burst traffic while enforcing average rate limits.
    """
    
    def __init__(
        self,
        requests_per_minute: int = 30,
        requests_per_hour: int = 500
    ):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        
        # Track requests per IP: {ip: [(timestamp, count), ...]}
        self.minute_requests: Dict[str, list] = defaultdict(list)
        self.hour_requests: Dict[str, list] = defaultdict(list)
    
    def _clean_old_requests(self, ip: str, window_seconds: int, storage: dict):
        """Remove requests outside the time window."""
        cutoff = time.time() - window_seconds
        storage[ip] = [t for t in storage[ip] if t > cutoff]
    
    def is_allowed(self, ip: str) -> Tuple[bool, str]:
        """
        Check if request is allowed for the given IP.
        Returns (allowed, reason).
        """
        now = time.time()
        
        # Clean old requests
        self._clean_old_requests(ip, 60, self.minute_requests)
        self._clean_old_requests(ip, 3600, self.hour_requests)
        
        # Check minute limit
        if len(self.minute_requests[ip]) >= self.requests_per_minute:
            wait_time = 60 - (now - self.minute_requests[ip][0])
            return False, f"Rate limit exceeded. Try again in {int(wait_time)} seconds."
        
        # Check hour limit
        if len(self.hour_requests[ip]) >= self.requests_per_hour:
            wait_time = 3600 - (now - self.hour_requests[ip][0])
            return False, f"Hourly limit exceeded. Try again in {int(wait_time/60)} minutes."
        
        # Record this request
        self.minute_requests[ip].append(now)
        self.hour_requests[ip].append(now)
        
        return True, "OK"
    
    def get_remaining(self, ip: str) -> dict:
        """Get remaining requests for the IP."""
        self._clean_old_requests(ip, 60, self.minute_requests)
        self._clean_old_requests(ip, 3600, self.hour_requests)
        
        return {
            "minute": {
                "remaining": self.requests_per_minute - len(self.minute_requests[ip]),
                "limit": self.requests_per_minute
            },
            "hour": {
                "remaining": self.requests_per_hour - len(self.hour_requests[ip]),
                "limit": self.requests_per_hour
            }
        }


# Global rate limiter instance
rate_limiter = RateLimiter(
    requests_per_minute=30,  # 30 requests per minute
    requests_per_hour=500    # 500 requests per hour
)


def get_client_ip(request: Request) -> str:
    """Extract client IP from request."""
    # Check for forwarded IP (behind proxy)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def check_rate_limit(request: Request):
    """
    Dependency to check rate limit.
    Raises HTTPException if limit exceeded.
    """
    ip = get_client_ip(request)
    allowed, reason = rate_limiter.is_allowed(ip)
    
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Too Many Requests",
                "message": reason,
                "remaining": rate_limiter.get_remaining(ip)
            }
        )
    
    return True
