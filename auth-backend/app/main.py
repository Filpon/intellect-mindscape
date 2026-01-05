import os
from typing import Any, Awaitable, Callable, Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIASGIMiddleware
from slowapi.util import get_remote_address

from app.caches.keydb import cache_span
from app.configs.logging_handler import configure_logging_handler
from app.middlewares.logging_middleware import LoggingMiddleware
from app.routers import auth
from app.services.keycloak import verify_permission
from app.utils.handlers import rate_limit_exceeded_handler

load_dotenv()  # Environmental variables

logger = configure_logging_handler()

ORIGINS: Optional[str] = os.getenv("ORIGINS")

# FastAPI app creation
app = FastAPI(docs_url="/api/v1/docs", openapi_url="/api/v1/openapi")
app.add_middleware(middleware_class=LoggingMiddleware)
logger.info("TESTING=%s", os.getenv("TESTING"))
if os.getenv("TESTING", "") != "true":
    logger.info("Include SlowAPIASGIMiddleware")
    limiter = Limiter(key_func=get_remote_address, application_limits=["9/5seconds"])
    app.add_middleware(middleware_class=SlowAPIASGIMiddleware)
    app.state.limiter = limiter


# Handling RateLimitExceeded exception
@app.exception_handler(RateLimitExceeded)
async def handle_rate_limit_exceeded(
    request: Request, exception_name: RateLimitExceeded
) -> Callable[[Request, Exception], Response | Awaitable[Response]] | JSONResponse:
    """
    Exception handling for RateLimitExceeded.

    This function is called when a request exceeds the allowed rate limit.
    It delegates the handling to the rate_limit_exceeded_handler

    :param request Request: The FastAPI request object
    :param exception_name RateLimitExceeded: The RateLimitExceeded exception instance
    :returns: JSONResponse with 429 status code and error message
    """
    return await rate_limit_exceeded_handler(_=request, __=exception_name)


app.include_router(auth.router, prefix="/api-auth/v1/auth", tags=["auth"])

# Configure CORS
origins = ORIGINS.split(sep=",") if ORIGINS else []
logger.info("ORIGINS=%s", ORIGINS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/check-auth")
async def root() -> Response:
    """
    API Healthcheck

    :returns Response: Response with sucessful status code
    """
    logger.info("Route availability check")
    return Response(status_code=status.HTTP_200_OK)


@app.get("/admin")  # Requires the admin role
def call_admin(
    user: dict[str, Any] = Depends(verify_permission(required_roles=["admin"])),
) -> str:
    """
    Admin role obtaining

    :param list required_roles: Role admin for calling
    :returns string: Messager for admin user
    """
    logger.info("Admin route availability check")
    return f"Hello, admin {user['preferred_username']}"


# Database creation
@app.on_event("startup")
async def startup() -> None:
    """
    Starting database creation

    """
    async with cache_span(app) as cache:
        app.state.cache = cache
        logger.info("Database creation was finished")


if __name__ == "__main__":
    import asyncio

    import uvicorn

    asyncio.run(uvicorn.run(app, host="0.0.0.0", port=8002))  # type: ignore[func-returns-value]
