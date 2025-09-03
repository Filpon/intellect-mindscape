from datetime import datetime
from typing import Any, Dict, List

from app.database.models import Game, GameModes, GameStatus
from app.database.repository.crud_base import CRUDBase
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDGame:
    @staticmethod
    async def get_by_id(db: AsyncSession, game_id: int) -> Game:
        return await CRUDBase.get_by_id(db=db, model=Game, id=game_id)

    @staticmethod
    async def create(db: AsyncSession, game_data: Dict[str, Any]) -> Game:
        return await CRUDBase.create(db=db, model=Game, obj_data=game_data)

    @staticmethod
    async def get_all_games(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Game]:
        return await CRUDBase.get_all(db=db, model=Game, skip=skip, limit=limit)

    @staticmethod
    async def get_all_game_modes_names(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Game]:
        game_modes_result = await CRUDBase.get_all(
            db=db, model=GameModes, skip=skip, limit=limit
        )
        game_modes_names = [game_mode.name for game_mode in game_modes_result]
        return game_modes_names

    @staticmethod
    async def get_all_distinct_by_column_name(
        db: AsyncSession, column_name: str
    ) -> List[Any]:
        """
        Retrieve all distinct values from a specified column in the Game model.

        :param db: The database session.
        :param column_name: The name of the column to retrieve distinct values from.
        :return: A list of distinct values from the specified column.
        """

        return await CRUDBase.fetch_all_distinct_by_column_name(
            db=db, model=Game, column_name=column_name
        )

    @staticmethod
    async def get_distinct_by_column_name_and_value(
        db: AsyncSession, column_name: str, value: Any
    ) -> List[Any]:
        return await CRUDBase.fetch_distinct_by_column_name_and_value(
            db=db, model=Game, column_name=column_name, value=value
        )

    @staticmethod
    async def fetch_distinct_games_by_filters(
        db: AsyncSession, filters: dict
    ) -> List[Any]:
        return await CRUDBase.fetch_distinct_by_filters(
            db=db, model=Game, filters=filters
        )

    @staticmethod
    async def update_game_result(
        db: AsyncSession, game_id: int, game_data: Dict[str, Any]
    ) -> Game:
        """
        Update an existing game result based on the provided game ID and data.
        """
        return await CRUDBase.update(db=db, model=Game, id=game_id, obj_data=game_data)

    @staticmethod
    async def get_in_progress_games_for_dates(
        db: AsyncSession, start_date: datetime, end_date: datetime
    ) -> List[Game]:
        filters = [
            {"condition": Game.status == GameStatus.in_progress},
            {"condition": Game.started_at >= start_date},
            {"condition": Game.started_at < end_date},
        ]
        return await CRUDBase.get_filtered(db, Game, filters)

    @staticmethod
    async def create_default_game_modes(db: AsyncSession):
        # Check if the default game modes already exist
        existing_modes = await CRUDBase.get_all(db, GameModes)
        if not existing_modes:
            try:
                # Create default game modes
                music_mode = GameModes(name="music")
                arithmetic_mode = GameModes(name="arithmetic")
                trigonometry_mode = GameModes(name="trigonometry")

                await CRUDBase.create(
                    db=db, model=GameModes, obj_data={"name": music_mode.name}
                )
                await CRUDBase.create(
                    db=db, model=GameModes, obj_data={"name": arithmetic_mode.name}
                )
                await CRUDBase.create(
                    db=db, model=GameModes, obj_data={"name": trigonometry_mode.name}
                )

            except IntegrityError:
                # Handle the case where the modes might already exist
                await db.rollback()
