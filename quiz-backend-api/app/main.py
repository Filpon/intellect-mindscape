import os
from pathlib import Path

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.configs.logging_handler import configure_logging_handler
from app.database.db import engine, get_db
from app.database.models import Base
from app.database.repository.game import CRUDGame
from app.routers import (
    game,
    remarks,
    stats,
    translations,
)
from app.services.counter_answers_validating import compare_and_update_answers_by_mode
from app.services.game_status_service import check_failed_games
from app.services.translation_service import load_translations_key_db

app = FastAPI(docs_url="/api/v1/docs", openapi_url="/api/v1/openapi")
scheduler = AsyncIOScheduler()

logger = configure_logging_handler()

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
KC_CLIENT_ID = os.getenv("KC_CLIENT_ID")
KC_CLIENT_SECRET_KEY = os.getenv("KC_CLIENT_SECRET_KEY")
ALGORITHM = "RS256"
AUDIENCE = f"{KEYCLOAK_URL}/protocol/openid-connect/userinfo"

ORIGINS = os.getenv("ORIGINS")
origins = ORIGINS.split(sep=",")

KEYDB_PASSWORD = os.getenv("KEYDB_PASSWORD")


# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database creation
@app.on_event("startup")
async def startup():
    """
    Starting database creation

    """
    game_modes_names = []

    async with engine.begin() as connector:
        await connector.run_sync(Base.metadata.create_all)

    # Create default game modes
    async for db in get_db():
        await CRUDGame.create_default_game_modes(db=db)
        game_modes_names = await CRUDGame.get_all_game_modes_names(db=db)

    load_translations_key_db(
        file_path=Path(__file__).resolve().parent / "utils" / "translations.json"
    )
    logger.info("Database creation was finished")
    scheduler.add_job(check_failed_games, "interval", minutes=1)
    for mode in game_modes_names:
        scheduler.add_job(
            compare_and_update_answers_by_mode, "interval", minutes=5, args=[mode]
        )
        logger.info("Scheduler job started for mode: %s", mode)
    scheduler.start()
    logger.info("Sheduler was started")
    logger.info("Game backend was started")


# Include routers
app.include_router(game.router, prefix="/api/v1/games", tags=["Game"])
app.include_router(
    translations.router, prefix="/api/v1/translations", tags=["Translations"]
)
app.include_router(remarks.router, prefix="/api/v1/remarks", tags=["Remarks"])
app.include_router(stats.router, prefix="/api/v1/stats", tags=["Stats"])


@app.get("/check-game")
async def root() -> Response:
    """
    API Healthcheck

    :returns Response: Response with sucessful status code
    """
    logger.info("Route availability check")
    return Response(status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8004)
