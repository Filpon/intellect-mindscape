from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.brokers.kafka import KafkaProducer
from app.database.db import get_db
from app.database.repository.game import CRUDGame
from app.database.schemas import GameRequest, GameResponse, GameResult
from app.services.game import (
    create_game,
    fetch_games,
    oauth2_scheme,
    update_game_result,
    verify_permission,
)

router = APIRouter()

game_crud = CRUDGame()

kafka_producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    topic="auth",
)


@router.post("/create", response_model=GameResponse)
async def create_game_result(
    game_request: GameRequest,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(oauth2_scheme),
):
    """
    Create new game result

    :param GameRequest game_request: The request object containing game details
    :param AsyncSession db: The database session dependency
    :param str _: The OAuth2 token dependency

    :return GameResponse: The created game response
    """
    user_sub_id = game_request.user_sub_id
    mode = game_request.mode
    latency_seconds = game_request.latency_seconds
    game_data = {
        "user_sub_id": user_sub_id,
        "mode_name": mode,
        "latency_seconds": latency_seconds,
        "status": "in_progress",
    }
    return await create_game(db=db, game_data=game_data)


@router.patch("/results")
async def submit_game_result(
    result: GameResult,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(oauth2_scheme),
):
    """
    Submit the result of completed game

    :param GameResult result: The result object containing game result details
    :param AsyncSession db: The database session dependency
    :param str _: The OAuth2 token dependency

    :return Any: The updated game result
    """
    return await update_game_result(
        db=db, game_id=result.id, game_data=result.dict()
    )


@router.get("/results")
async def fetch_games_results(
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(verify_permission(["admin"])),
):
    """
    Fetch all results

    The route retrieves a list of game results from the database.

    :param _ dict: A dictionary containing the request context, used for permission verification

    :returns List[Dict[str, Any]]: List of users dictionaries
    """
    return await fetch_games(db=db)
