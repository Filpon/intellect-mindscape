import os
from typing import Final

from app.configs.logging_handler import configure_logging_handler
from app.kafka.kafka_consumer import KafkaConsumer
from app.utils.process_results import ResultsProcessing
from dotenv import load_dotenv

logger = configure_logging_handler()

load_dotenv()

KAFKA_HOSTNAME: Final[str] = os.getenv("KAFKA_HOSTNAME")
KAFKA_PORT: Final[str] = os.getenv("KAFKA_PORT")


async def process_game_messages(consumer: KafkaConsumer):
    """
    Receive messages from a Kafka topic and process them.

    This function consumes messages from the Kafka topic, processes the results,
    and generates recommendations based on the game results.

    :param db: Database session
    :param consumer: Kafka consumer instance
    :return dict: Response indicating the status of the processing
    """
    logger.info("Processing game messages")
    # Consume messages from Kafka
    game_results = await consumer.consume_messages_list()

    # Organize the results
    organized_results = await ResultsProcessing.order_game_results(
        game_results=game_results
    )

    # Process the organized results
    await ResultsProcessing.process_game_results(
        game_results=organized_results, collection_name="game_recommendations"
    )

    # Generate statistics from the processed results
    statistics = await ResultsProcessing.generate_statistics(
        collection_name="game_recommendations"
    )

    # Generate recommendations based on the statistics
    recommendation_results = await ResultsProcessing.generate_recommendations(
        statistics=statistics
    )

    return {
        "status": "success",
        "message": f"Generated recommendation results are {recommendation_results}",
    }
