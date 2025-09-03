import os
from typing import Final

from app.kafka.kafka_consumer import get_consumer
from app.services.create_recommendations import process_game_messages
from dotenv import load_dotenv
from fastapi import APIRouter, Depends

load_dotenv()

KAFKA_HOSTNAME: Final[str] = os.getenv("KAFKA_HOSTNAME")
KAFKA_PORT: Final[str] = os.getenv("KAFKA_PORT")

router = APIRouter()


@router.get("/receive")
async def receive_recommendataion(
    consumer=Depends(get_consumer),
) -> dict:
    """
    Receiving recommendations.
    The asynchronous router takes message body content as input
    and sends it to the specified Kafka topic using the Kafka producer

    :param consumer: Application consumer state

    :return dict: Response indicating the status of the sending message
    """
    return await process_game_messages(consumer=consumer)
