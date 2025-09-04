import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.configs.logging_handler import configure_logging_handler

load_dotenv()

logger = configure_logging_handler()

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL")

# Async engine creation
engine = create_async_engine(url=DATABASE_URL, echo=True)

# Sessionmaker creation
ASYNC_SESSION_LOCAL = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncSession:
    """
    Session obtaining for service functionality

    :yield AsyncSession session: Asynchronious session object
    """
    async with ASYNC_SESSION_LOCAL() as session:
        yield session
    logger.info("Database session was created")
