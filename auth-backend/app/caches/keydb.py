import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Final

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.configs.logging_handler import configure_logging_handler
from redis import asyncio as aioredis

load_dotenv()

logger = configure_logging_handler()

KEYDB_PASSWORD: Final[str] = os.getenv("KEYDB_PASSWORD")
KEYDB_PORT: Final[str] = os.getenv("KEYDB_PORT")


@asynccontextmanager
async def cache_span(_: FastAPI) -> AsyncIterator[None]:
    """
    Asynchronous context manager for initializing FastAPI caching

    This context manager establishes connection to cache database instance
    and initializes the FastAPI cache with the specified backend

    :param _: FastAPI: The FastAPI application instance. This parameter is
    not used within the context manager but it is included for
    compatibility with FastAPI's dependency injection system

    :yield: The context manager yields control back to the caller
    after initializing the cache. The cache availability within
    the context block
    """
    keydb = aioredis.from_url(f"redis://:{KEYDB_PASSWORD}@keydb:{KEYDB_PORT}")
    FastAPICache.init(backend=RedisBackend(keydb), prefix="fastapi-cache")
    yield FastAPICache.get_backend()


async def get_cache(request: Request):
    """
    Dependency function to retrieve the KeyDB cache from the FastAPI application state

    :param Request request: The FastAPI request object, which provides access
    to the application state

    :returns: The KeyDB cache instance stored in the application state
    """
    logger.info("Application cache instance was used")
    return request.app.state.cache
