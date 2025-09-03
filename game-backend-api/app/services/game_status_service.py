# In app/services/game_status_service.py

from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.configs.logging_handler import configure_logging_handler
from app.database.db import get_db
from app.database.models import GameStatus
from app.database.repository.game import CRUDGame

logger = configure_logging_handler()

# Initialize the scheduler
scheduler = AsyncIOScheduler()


async def check_failed_games():
    logger.info("Sheduler started !!!!!!")
    async for db in get_db():
        game_crud = CRUDGame()
        # Get the current time
        current_time = datetime.now(timezone.utc)

        # Define the start and end of today
        today_start = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        # Define the start and end of the day before yesterday
        day_before_yesterday_start = today_start - timedelta(days=2)
        day_before_yesterday_end = today_start - timedelta(days=1)

        # Fetch in-progress games for today and the day before yesterday
        games_today = await game_crud.get_in_progress_games_for_dates(
            db, today_start, today_end
        )
        games_day_before_yesterday = await game_crud.get_in_progress_games_for_dates(
            db, day_before_yesterday_start, day_before_yesterday_end
        )

        # Combine the results
        all_games = games_today + games_day_before_yesterday

        for game in all_games:
            # Check if the game has been in progress for more than an hour
            if game.started_at < (current_time - timedelta(hours=1)):
                # Update the game status to "failed"
                game_data = {"status": GameStatus.failed}
                await game_crud.update_game_result(
                    db=db, game_id=game.id, game_data=game_data
                )
                logger.info("Game ID %s status updated to 'failed'.", game.id)


def start_scheduler():
    # Schedule the check_failed_games function to run every 15 minutes
    scheduler.add_job(check_failed_games, "interval", minutes=1)
    scheduler.start()


if __name__ == "__main__":
    start_scheduler()
    # Keep the script running
    import asyncio

    asyncio.get_event_loop().run_until_complete()
