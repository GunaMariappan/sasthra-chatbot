import threading
import time
from collections import defaultdict, deque

from fastapi import Depends, HTTPException, Request

from app.api.deps import get_current_user
from app.core.config import settings


class RateLimiter:
    """Allows max_requests per window_seconds for each key. Kept in memory."""

    def __init__(self, max_requests: int, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.hits: dict[str, deque] = defaultdict(deque)
        self.lock = threading.Lock()

    def check(self, key: str) -> None:
        now = time.monotonic()

        with self.lock:
            if len(self.hits) > 5000:
                self._cleanup(now)

            queue = self.hits[key]
            while queue and now - queue[0] > self.window_seconds:
                queue.popleft()

            if len(queue) >= self.max_requests:
                retry_after = int(self.window_seconds - (now - queue[0])) + 1
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests. Please try again in a minute.",
                    headers={"Retry-After": str(retry_after)},
                )

            queue.append(now)

    def _cleanup(self, now: float) -> None:
        stale = [k for k, q in self.hits.items() if not q or now - q[-1] > self.window_seconds]
        for key in stale:
            del self.hits[key]


auth_limiter = RateLimiter(settings.RATE_LIMIT_AUTH_PER_MINUTE)
chat_limiter = RateLimiter(settings.RATE_LIMIT_CHAT_PER_MINUTE)


def auth_rate_limit(request: Request) -> None:
    """For /signup and /login: limit per client IP address."""
    ip = request.client.host if request.client else "unknown"
    auth_limiter.check(f"{request.url.path}:{ip}")


def chat_rate_limit(current_user: dict = Depends(get_current_user)) -> dict:
    """For /chatbot: limit per logged-in user. Returns the user for the route."""
    chat_limiter.check(str(current_user["_id"]))
    return current_user