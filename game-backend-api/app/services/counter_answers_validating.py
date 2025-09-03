from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database.db import get_db
from app.database.repository.game import CRUDGame
from app.configs.logging_handler import configure_logging_handler
from app.utils.keydb import keydb_instance

logger = configure_logging_handler()
scheduler = AsyncIOScheduler()
game_crud = CRUDGame()


async def compare_and_update_answers_by_mode(mode: str):
    logger.info("Scheduler started to compare and update answers for mode %s", mode)
    async for db in get_db():
        # Fetch all user_sub_ids
        user_sub_ids = await game_crud.get_all_distinct_by_column_name(
            db=db, column_name="user_sub_id"
        )
        user_sub_id_sql_db_scores = {"correct_score": 0, "incorrect_score": 0}
        for user_sub_id in user_sub_ids:
            completed_games = await game_crud.fetch_distinct_games_by_filters(
                db=db,
                filters={
                    "user_sub_id": user_sub_id,
                    "mode_name": mode,
                    "status": "completed",
                },
            )
            for game in completed_games:
                user_sub_id_sql_db_scores["correct_score"] += game.correct_score
                user_sub_id_sql_db_scores["incorrect_score"] += game.incorrect_score
            cache_db_key = f"{user_sub_id}--{mode}"
            retrieved_entry = keydb_instance.hgetall(cache_db_key)
            if retrieved_entry:
                user_sub_id_cache_db_scores = {
                    k.decode("utf-8"): v.decode("utf-8")
                    for k, v in retrieved_entry.items()
                }
            else:
                user_sub_id_cache_db_scores = {"correct_score": 0, "incorrect_score": 0}

            if (
                user_sub_id_sql_db_scores["correct_score"]
                != user_sub_id_cache_db_scores["correct_score"]
                or user_sub_id_sql_db_scores["incorrect_score"]
                != user_sub_id_cache_db_scores["incorrect_score"]
            ):
                keydb_instance.hset(
                    cache_db_key,
                    mapping={
                        "mode": mode,
                        "correct_score": user_sub_id_sql_db_scores["correct_score"],
                        "incorrect_score": user_sub_id_sql_db_scores["incorrect_score"],
                    },
                )
    logger.info("Scheduler finished to compare and update answers for mode %s", mode)
