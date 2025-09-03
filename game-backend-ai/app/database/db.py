import os

from app.configs.logging_handler import configure_logging_handler
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

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


async def execute_raw_sql(query: str, params: dict = None) -> list:
    """
    Executing raw SQL query

    :param str query: The SQL query to execute
    :param dict params: Optional parameters for the SQL query

    :return list: List of results from the query
    """
    async with ASYNC_SESSION_LOCAL() as session:
        result = await session.execute(text(query), params)
        return result.fetchall()
