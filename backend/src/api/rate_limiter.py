import time
from typing import Dict, Optional
from collections import defaultdict
from fastapi import HTTPException, Request
import asyncio


class InMemoryRateLimiter:
    """
    Simple in-memory rate limiter for API requests
    In production, use Redis or similar for distributed rate limiting
    """

    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)  # user_id -> [timestamps]
        self.limits = {
            'requests_per_minute': 60,  # Max 60 requests per minute per user
            'requests_per_hour': 500,   # Max 500 requests per hour per user
            'concurrent_requests': 5    # Max 5 concurrent requests per user
        }

    def is_allowed(self, user_id: str) -> bool:
        """
        Check if a request from user_id is allowed based on rate limits
        """
        current_time = time.time()

        # Clean old requests (older than 1 hour)
        self.requests[user_id] = [
            timestamp for timestamp in self.requests[user_id]
            if current_time - timestamp < 3600  # 1 hour
        ]

        # Check minute limit
        minute_requests = [
            timestamp for timestamp in self.requests[user_id]
            if current_time - timestamp < 60  # 1 minute
        ]

        if len(minute_requests) >= self.limits['requests_per_minute']:
            return False

        # Add current request
        self.requests[user_id].append(current_time)

        return True

    def get_remaining_requests(self, user_id: str) -> int:
        """
        Get number of remaining requests for the user in the current minute
        """
        current_time = time.time()
        minute_requests = [
            timestamp for timestamp in self.requests[user_id]
            if current_time - timestamp < 60
        ]
        return max(0, self.limits['requests_per_minute'] - len(minute_requests))


# Global rate limiter instance
rate_limiter = InMemoryRateLimiter()


def get_client_ip(request: Request) -> str:
    """
    Extract client IP from request
    """
    # Check for forwarded IP headers first
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()

    # Fallback to client host
    if request.client and request.client.host:
        return request.client.host

    return "unknown"


async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware to apply rate limiting to API requests
    """
    client_ip = get_client_ip(request)

    # Skip rate limiting for health check endpoints
    if request.url.path == "/health":
        response = await call_next(request)
        return response

    # Check if request is allowed
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )

    response = await call_next(request)

    # Add rate limit headers to response
    remaining = rate_limiter.get_remaining_requests(client_ip)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Limit"] = str(rate_limiter.limits['requests_per_minute'])

    return response


def validate_request_data(data: dict) -> bool:
    """
    Validate request data to ensure it meets requirements
    """
    if not data:
        return False

    # Check for required fields depending on the endpoint
    # This is a simplified validation - in practice, you'd have more specific validation
    if 'content' in data:
        content = data['content']
        if not isinstance(content, str) or len(content.strip()) == 0:
            return False
        if len(content) > 10000:  # Max 10k characters
            return False

    if 'selected_text' in data:
        selected_text = data['selected_text']
        if isinstance(selected_text, str) and len(selected_text) > 5000:  # Max 5k characters
            return False

    return True