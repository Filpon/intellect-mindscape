from app.database.models import Stats
from app.database.repository.crud_base import CRUDBase
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDStats:
    @staticmethod
    async def update_stats(db: AsyncSession, user_id: int, correct: bool) -> Stats:
        """
        Update the statistics for the user based on whether their answer was correct.

        This method retrieves the user's statistics, increments the count of correct or incorrect answers,
        and commits the changes to the database

        :param AsyncSession db: The database session
        :param int user_id: The ID of the user whose statistics are to be updated
        :param bool correct: A boolean indicating whether the user's answer was correct
        :return Stats: The updated statistics object for the user
        """
        stats = await CRUDBase.get_by_id(db, Stats, user_id)
        if correct:
            stats.correct_answers += 1
        else:
            stats.incorrect_answers += 1
        db.add(stats)
        await db.commit()
        await db.refresh(stats)
        return stats
