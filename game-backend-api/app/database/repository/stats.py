from app.database.models import Stats
from app.database.repository.crud_base import CRUDBase
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDStats:
    @staticmethod
    async def update_stats(db: AsyncSession, user_id: int, correct: bool) -> Stats:
        stats = await CRUDBase.get_by_id(db, Stats, user_id)
        if correct:
            stats.correct_answers += 1
        else:
            stats.incorrect_answers += 1
        db.add(stats)
        await db.commit()
        await db.refresh(stats)
        return stats
