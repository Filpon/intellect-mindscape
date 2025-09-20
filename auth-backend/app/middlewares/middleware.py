from collections import defaultdict
from time import perf_counter
from typing import Callable

from fastapi import status, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """
    Middleware limiting the rate of requests from clients

    The middleware tracks the number of requests made by each client
    IP address within specified time window and restricts application access
    if the limit is exceeded
    """

    def __init__(
        self,
        app: Callable,  # type: ignore[type-arg]
        max_requests: int = 100,
        time_window: int = 60,
    ) -> None:
        """
        Initializes the RateLimiterMiddleware

        :param app: The FastAPI application instance
        :param int max_requests: The maximum number of requests allowed within the
                             time window
        :param int time_window: The time window in seconds for counting requests
        """
        super().__init__(app)
        self.max_requests: int = max_requests
        self.time_window: int = time_window
        self.requests: dict[str, list[float]] = defaultdict(
            list
        )

    async def dispatch(
            self,
            request: Request,
            call_next: Callable,  # type: ignore[type-arg]
        ) -> JSONResponse:
        """
        Processes the incoming request and applies rate limiting.
        This method checks the number of requests made
        by the client IP within the defined time window.
        If the limit is exceeded, 429 Too Many Requests Error response
        is returned.

        :param Request request: The incoming request object
        :param call_next: Function to call the next middleware or endpoint
        :return JSONResponse: The response object
        """
        client_ip = request.client.host  # type: ignore[union-attr]
        current_time = perf_counter()

        # Remove old requests
        self.requests[client_ip] = [
            t for t in self.requests[client_ip] if current_time - t < self.time_window
        ]

        if len(self.requests[client_ip]) >= self.max_requests:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"message": "Too Many Requests"},
            )

        self.requests[client_ip].append(current_time)

        response = await call_next(request)
        return response  # type: ignore[no-any-return]
