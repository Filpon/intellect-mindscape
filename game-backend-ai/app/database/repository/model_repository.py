from typing import Generic, List, TypeVar

from app.database.models import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

ModelType = TypeVar("ModelType", bound=Base)  # pylint: disable=C0103


class ModelRepository(Generic[ModelType]):
    """
    Database model repository for CRUD operations.
    """

    def __init__(self, session: AsyncSession, model: ModelType):
        """
        Initialize the ModelRepository instance

        :param AsyncSession session: Current database session
        :param ModelType model: Database model name
        """
        self.session = session
        self.model = model

    async def fetch_by_filters(self, **filters) -> List[ModelType]:
        """
        Fetching results by filters

        :param filters: Field-value pairs for filtering

        :return List[ModelType]: Filtered results
        """
        query = select(self.model)
        for field, value in filters.items():
            if hasattr(self.model, field):
                query = query.where(
                    getattr(self.model, field).ilike(f"%{value}%")
                )  # Case-insensitive search
        result = await self.session.execute(query)
        return result.scalars().all()

    async def fetch_all(self) -> List[ModelType]:
        """
        Fetching all results

        :return List[ModelType]: Fetched results
        """
        result = await self.session.execute(select(self.model))
        return result.scalars().all()
