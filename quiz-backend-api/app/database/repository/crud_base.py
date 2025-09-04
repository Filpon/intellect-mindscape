from typing import Any, Dict, Generic, List, TypeVar

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    """Base class for CRUD operations."""

    @staticmethod
    async def get_by_id(db: AsyncSession, model: ModelType, id: int) -> ModelType:
        """
        Retrieve an object by ID.
        """
        result = await db.execute(select(model).where(model.id == id))
        obj = result.scalars().first()
        if obj is None:
            raise NoResultFound(f"{model.__name__} with ID {id} not found.")
        return obj

    @staticmethod
    async def get_all(
        db: AsyncSession, model: ModelType, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Retrieve a list of objects.
        """
        result = await db.execute(select(model).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def fetch_all_distinct_by_column_name(
        db: AsyncSession, model: ModelType, column_name: str
    ) -> List[Any]:
        """
        Retrieve all distinct values from a specified column in the Game model.

        :param db: The database session.
        :param column_name: The name of the column to retrieve distinct values from.
        :return: A list of distinct values from the specified column.
        """
        # Ensure the column name is valid
        if not hasattr(model, column_name):
            raise ValueError(
                f"Column '{column_name}' does not exist in the Game model."
            )

        # Create a query to select distinct values from the specified column
        result = await db.execute(select(getattr(model, column_name)).distinct())

        return result.scalars().all()

    @staticmethod
    async def fetch_distinct_by_column_name_and_value(
        db: AsyncSession, model: ModelType, column_name: str, value: Any
    ) -> List[Any]:
        """
        Retrieve distinct values from a specified column in the model
        where another column matches a specific value.

        :param db: The database session.
        :param model: The model class to query.
        :param column_name: The name of the column to retrieve distinct values from.
        :param value: The value to filter the results by.
        :return: A list of distinct values from the specified column.
        """
        # Ensure the column name is valid
        if not hasattr(model, column_name):
            raise ValueError(
                f"Column '{column_name}' does not exist in the {model.__name__} model."
            )

        # Create a query to select distinct values from the specified column
        query = select(model).distinct().where(getattr(model, column_name) == value)
        result = await db.execute(query)

        # Extract the distinct values from the result
        return result.scalars().all()

    @staticmethod
    async def fetch_distinct_by_filters(
        db: AsyncSession, model: ModelType, filters: dict
    ) -> List[Any]:
        """
        Retrieve distinct values from the model where multiple columns match their respective values.

        :param db: The database session.
        :param model: The model class to query.
        :param filters: A dictionary where keys are column names and values are the values to filter by.
        :return: A list of distinct rows from the model that match the specified filters.
        """
        # Ensure all column names are valid
        for column_name in filters.keys():
            if not hasattr(model, column_name):
                raise ValueError(
                    f"Column '{column_name}' does not exist in the {model.__name__} model."
                )

        # Create a query to select distinct rows where all specified columns match their values
        query = select(model).distinct()

        # Build the where clause dynamically
        for column_name, value in filters.items():
            query = query.where(getattr(model, column_name) == value)

        result = await db.execute(query)

        # Extract the distinct values from the result
        return result.scalars().all()

    @staticmethod
    async def create(
        db: AsyncSession, model: ModelType, obj_data: Dict[str, Any]
    ) -> ModelType:
        """
        Create a new object.
        """
        obj = model(**obj_data)
        db.add(obj)
        try:
            await db.commit()
            await db.refresh(obj)
        except IntegrityError:
            await db.rollback()
            raise IntegrityError(f"{model.__name__} already exists.")
        return obj

    @staticmethod
    async def update(
        db: AsyncSession, model: ModelType, id: int, obj_data: Dict[str, Any]
    ) -> ModelType:
        """
        Update an existing object.
        """
        obj = await CRUDBase.get_by_id(db, model, id)

        for key, value in obj_data.items():
            setattr(obj, key, value)

        db.add(obj)
        try:
            await db.commit()
            await db.refresh(obj)
        except IntegrityError:
            await db.rollback()
            raise IntegrityError(f"Error updating {model.__name__} with ID {id}.")

    @staticmethod
    async def get_filtered(
        db: AsyncSession, model: ModelType, filters: List[Dict[str, Any]]
    ) -> List[ModelType]:
        """
        Retrieve a list of objects based on filters.
        """
        query = select(model)
        for filter_instance in filters:
            query = query.where(filter_instance["condition"])
        result = await db.execute(query)
        return result.scalars().all()
