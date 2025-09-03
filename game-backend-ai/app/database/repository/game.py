from collections import defaultdict
from uuid import UUID

from app.database.db import execute_raw_sql


class CRUDGame:
    """
    Class for handling CRUD operations related to games in the database

    The class provides methods to fetch user IDs associated with games and 
    retrieve completed games along with their scores
    """
    @staticmethod
    async def fetch_user_id_with_games() -> list[UUID]:
        """
        Fetches list of user IDs
        
        :return list[UUID]: The list where user identificators with
        at least one started game are presented
        """
        query = "SELECT DISTINCT id, user_sub_id FROM games"
        results = await execute_raw_sql(query)

        # Create a defaultdict to hold lists of ids for each user_sub_id
        user_sub_id_dict = defaultdict(list)

        # Populate the dictionary
        for row in results:
            game_id, user_sub_id = row
            user_sub_id_dict[user_sub_id].append(game_id)

        # Convert defaultdict to a regular dictionary
        return {
            game_id: str(user_sub_id)
            for user_sub_id, game_ids in user_sub_id_dict.items()
            for game_id in game_ids
        }  # Extracting the first column from each row

    @staticmethod
    async def fetch_completed_games_with_scores(user_sub_id: str) -> list:
        """
        Fetches scores of completed games
        
        :return list: The list with user correct scores and
        incorrect scores 
        """

        query = """
        SELECT correct_score, incorrect_score FROM games 
        WHERE user_sub_id = :user_sub_id AND status = 'completed'
        """
        params = {"user_sub_id": user_sub_id}
        return await execute_raw_sql(query, params)
