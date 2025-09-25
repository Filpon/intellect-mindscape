import os
from typing import Final

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import (
    KafkaConnectionError,
    KafkaError,
    KafkaTimeoutError,
)
from app.configs.logging_handler import configure_logging_handler
from dotenv import load_dotenv
from fastapi import HTTPException, Request, status

logger = configure_logging_handler()

load_dotenv()

KAFKA_HOSTNAME: Final[str] = os.getenv("KAFKA_HOSTNAME")
KAFKA_PORT: Final[str] = os.getenv("KAFKA_PORT")


class KafkaConsumer:
    """
    Managing Kafka topics using Kafka Consumer

    This class provides methods for starting the connection to the Kafka container
    and consuming messages from Kafka topics, as well as to start and stop the Kafka consumer
    """

    def __init__(self, bootstrap_servers: str, topic: str):
        """
        Initialize the KafkaConsumer instance

        :param str bootstrap_servers: Kafka connecting server
        :param str topic: Kafka topic name
        :param str group_id: Kafka consumer group ID
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
         )

    async def start(self):
        """
        Create an active Kafka consumer
        """
        try:
            if self.consumer:
                await self.consumer.start()
                logger.info("Kafka consumer instance was started")
            return self.consumer
        except KafkaTimeoutError as error:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Timeout Kafka connection error",
            ) from error
        except KafkaConnectionError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to connect to Kafka server",
            ) from error
        except Exception as exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to start Kafka consumer, because of {str(exception)}",
            ) from exception

    async def consume_messages_list(
        self, timeout_ms: int = 1000, max_records_limit: int = 10000
    ) -> None:
        """
        Consume messages from the Kafka topic

        :param Callable callback: A function to process the consumed messages
        """
        messages = []
        try:
            records = await self.consumer.getmany(
                timeout_ms=timeout_ms, max_records=max_records_limit
            )
            for _, messages in records.items():
                for message in messages:
                    logger.info("Consumed message: %s", message.value.decode('utf-8'))

            return messages

        except KafkaConnectionError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Common base broker error - {str(error)}",
            ) from error
        except Exception as exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to consume message from Kafka, because of {str(exception)}",
            ) from exception

    async def stop(self):
        """
        Stop the Kafka consumer
        """
        try:
            if self.consumer:
                await self.consumer.stop()
        except KafkaError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Common base broker error - {str(error)}",
            ) from error
        except Exception as exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(exception),
            ) from exception


async def get_consumer(request: Request):
    """
    Dependency function to retrieve the Kafka consumer from the FastAPI application state.
    This function accesses the application state to obtain the Kafka consumer instance,
    which can be used in route handlers for consuming messages from Kafka topics

    :param Request request: The FastAPI request object, which provides access
    to the application state

    :returns: The Kafka consumer instance stored in the application state
    """
    return request.app.state.consumer


kafka_consumer = KafkaConsumer(
    bootstrap_servers=f"{KAFKA_HOSTNAME}:{KAFKA_PORT}",
    topic="quiz-answers",
)
