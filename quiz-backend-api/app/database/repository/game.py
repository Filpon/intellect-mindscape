from datetime import datetime
from typing import Any, Dict, List

from app.database.models import Game, GameModes, GameStatus
from app.database.repository.crud_base import CRUDBase
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDGame:
    @staticmethod
    async def get_by_id(db: AsyncSession, game_id: int) -> Game:
        """
        Retrieve game by its ID

        :param AsyncSession db: The database session
        :param int game_id: The ID of the game to retrieve
        :return Game: The game object corresponding to the provided ID
        """
        return await CRUDBase.get_by_id(db=db, model=Game, id=game_id)

    @staticmethod
    async def create(db: AsyncSession, game_data: Dict[str, Any]) -> Game:
        """
        Create new game

        :param AsyncSession db: The database session
        :param Dict[str, Any] game_data: The data for the game to be created
        :return Game: The created game object
        """
        return await CRUDBase.create(db=db, model=Game, obj_data=game_data)

    @staticmethod
    async def get_all_games(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Game]:
        """
        Retrieve all games with pagination

        :param AsyncSession db: The database session
        :param int skip: The number of records to skip
        :param int limit: The maximum number of records to return

        :return List[Game]: List of game objects
        """
        return await CRUDBase.get_all(db=db, model=Game, skip=skip, limit=limit)

    @staticmethod
    async def get_all_game_modes_names(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Game]:
        """
        Retrieve names of all game modes

        :param AsyncSession db: The database session
        :param int skip: The number of records to skip
        :param int limit: The maximum number of records to return

        :return List[Game]: List of distinct values
        """
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
        Retrieve all distinct values from a specified column in the Game model

        :param AsyncSession db: The database session
        :param str column_name: The name of the column to retrieve distinct values from

        :return List[Any]: List of distinct values from the specified column
        """

        return await CRUDBase.fetch_all_distinct_by_column_name(
            db=db, model=Game, column_name=column_name
        )

    @staticmethod
    async def get_distinct_by_column_name_and_value(
        db: AsyncSession, column_name: str, value: Any
    ) -> List[Any]:
        """
        Retrieve distinct values from a specified column based on a given value

        :param AsyncSession db: The database session
        :param str column_name: The name of the filtered column
        :param Any value: The value to filter by

        :return List[Any]: List of distinct values matching the criteria
        """
        return await CRUDBase.fetch_distinct_by_column_name_and_value(
            db=db, model=Game, column_name=column_name, value=value
        )

    @staticmethod
    async def fetch_distinct_games_by_filters(
        db: AsyncSession, filters: dict
    ) -> List[Any]:
        """
        Fetch distinct games based on provided filters

        :param AsyncSession db: The database session
        :param dict filters: The filters to apply when fetching games

        :return List[Any]: List of distinct games matching the filters
        """
        return await CRUDBase.fetch_distinct_by_filters(
            db=db, model=Game, filters=filters
        )

    @staticmethod
    async def update_game_result(
        db: AsyncSession, game_id: int, game_data: Dict[str, Any]
    ) -> Game:
        """
        Update an existing game result based on the provided game ID and data.

        :param AsyncSession db: The database session
        :param int game_id: The ID of the game to update
        :param Dict[str, Any] game_data: The data to update the game with

        :return Game: The updated game object
        """
        return await CRUDBase.update(db=db, model=Game, id=game_id, obj_data=game_data)

    @staticmethod
    async def get_in_progress_games_for_dates(
        db: AsyncSession, start_date: datetime, end_date: datetime
    ) -> List[Game]:
        """
        Retrieve games that are in progress within a specified date range

        :param AsyncSession db: The database session
        :param datetime start_date: The start date for filtering games
        :param datetime end_date: The end date for filtering games
        :return List[Game]: A list of games that are in progress within the specified date range
        """
        filters = [
            {"condition": Game.status == GameStatus.in_progress},
            {"condition": Game.started_at >= start_date},
            {"condition": Game.started_at < end_date},
        ]
        return await CRUDBase.get_filtered(db, Game, filters)

    @staticmethod
    async def create_default_game_modes(db: AsyncSession):
        """
        Default game modes creation if they do not already exist

        :param AsyncSession db: The database session
        """
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
