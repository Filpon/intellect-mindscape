from typing import Any, Dict

from app.database.models import User
from app.database.repository.crud_base import CRUDBase
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDUser:
    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> User:
        return await CRUDBase.get_by_id(db, User, user_id)

    @staticmethod
    async def create(db: AsyncSession, user_data: Dict[str, Any]) -> User:
        return await CRUDBase.create(db, User, user_data)
