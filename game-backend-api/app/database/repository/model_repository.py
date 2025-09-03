from typing import Generic, TypeVar

from app.database.models import Base
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

ModelType = TypeVar("ModelType", bound=Base)  # pylint: disable=C0103


class ModelRepository(Generic[ModelType]):
    """
    Database model repository for CRUD operations.
    """

    def __init__(self, session: AsyncSession, model: ModelType):
        self.session = session
        self.model = model

    async def fetch_by_id(self, id: int) -> ModelType:
        """
        Fetching results by ID.

        :param id: Identificator for filtering.
        :type id: int
        :raises NoResultFound: If no record is found with the given ID.
        :return: Filtered results.
        :rtype: ModelType
        """
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        record = result.scalars().first()
        if record is None:
            raise NoResultFound(f"{self.model.__name__} with ID {id} not found.")
        return record

    async def fetch_by_filters(self, **filters) -> list[ModelType]:
        """
        Fetching results by filters.

        :param filters: Field-value pairs for filtering.
        :return: Filtered results.
        :rtype: list[ModelType]
        """
        query = select(self.model)
        for field, value in filters.items():
            if hasattr(self.model, field):
                query = query.where(
                    getattr(self.model, field).ilike(f"%{value}%")
                )  # Case-insensitive search
        result = await self.session.execute(query)
        return result.scalars().all()

    async def fetch_all(self) -> list[ModelType]:
        """
        Fetching all results.

        :return: Fetched results.
        :rtype: list[ModelType]
        """
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def create(self, obj: dict) -> ModelType:
        """
        Record creation.

        :param obj: Object creation.
        :type obj: schemas.BaseSchema
        :raises IntegrityError: If the record already exists.
        :return: Created object.
        :rtype: ModelType
        """
        instance = self.model(**obj.dict())
        self.session.add(instance)
        try:
            await self.session.commit()
            await self.session.refresh(instance)
        except IntegrityError:
            await self.session.rollback()
            raise IntegrityError(
                f"{self.model.__name__} with provided data already exists."
            )
        return instance
