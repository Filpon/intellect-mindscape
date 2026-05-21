import asyncio

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import (
    ConsumerStoppedError,
    KafkaConnectionError,
    KafkaError,
    KafkaTimeoutError,
    NoBrokersAvailable,
    UnknownTopicOrPartitionError,
)
from fastapi import HTTPException, status

from app.configs.logging_handler import configure_logging_handler

logger = configure_logging_handler()


class KafkaProducer:
    """
    Kafka producer for sending messages to a specified topic
    """

    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        """
        Initializes kafka producer instance

        :param str bootstrap_servers: The Kafka server bootstrap address
        :param str topic: The topic to which messages will be sent
        """
        self.bootstrap_servers: str = bootstrap_servers
        self.topic: str = topic
        self.producer: None | AIOKafkaProducer = None

    async def start(self) -> None:
        """
        Start the Kafka producer

        Initializes the AIOKafkaProducer and connects to the Kafka server
        """
        try:
            if self.producer is None:
                self.producer = AIOKafkaProducer(
                    bootstrap_servers=self.bootstrap_servers
                )
            await self.producer.start()
        except KafkaConnectionError as error:
            logger.exception("Unable to connect to Kafka server")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to connect to Kafka server",
            ) from error
        except Exception as exception:
            logger.exception("Failed to start Kafka, because of %s", exception)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to start Kafka, because of {str(exception)}",
            ) from exception

    async def produce_message(self, key: str, value: str) -> None:
        """
        Produce message to the Kafka topic

        :param key: The key for the message
        :param value: The value of the message
        """
        if self.producer is None:
            logger.error("Producer is not started")
            return None
        if isinstance(value, str):
            value = value.encode("utf-8")
        try:
            await self.producer.send_and_wait(
                self.topic, key=key.encode(), value=value.encode()
            )
            logger.info("Message delivered to %s", self.topic)
        except KafkaTimeoutError as excp:
            logger.error("Message delivery timed out: %s", excp)
        except UnknownTopicOrPartitionError as excp:
            logger.error("Unknown topic or partition: %s", excp)
        except KafkaError as excp:
            logger.error("Kafka error: %s", excp)
        except Exception as excp:  # pylint: disable=W0718
            logger.error("Message delivery failed: %s", excp)

    async def stop(self) -> None:
        """
        Close the producer
        """
        if self.producer is not None:
            await self.producer.stop()


class KafkaConsumer:
    """
    Kafka consumer for consuming messages from specified topic
    """

    def __init__(self, bootstrap_servers: str, topic: str, group_id: str) -> None:
        """
        Initializes Kafka Consumer and connects to the Kafka server

        :param str bootstrap_servers: The Kafka server address
        :param str topic: The topic from which messages will be consumed
        :param str group_id: The consumer group ID
        """
        self.bootstrap_servers: str = bootstrap_servers
        self.topic: str = topic
        self.group_id: str = group_id
        self.consumer: AIOKafkaConsumer | None = None

    async def start(self) -> None:
        """
        Start Kafka consumer
        """
        try:
            if self.consumer is not None:
                self.consumer = AIOKafkaConsumer(
                    self.topic,
                    bootstrap_servers=self.bootstrap_servers,
                    group_id=self.group_id,
                    auto_offset_reset="earliest",
                )
            await self.consumer.start()
        except KafkaConnectionError as error:
            logger.exception("Unable to connect to Kafka server")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to connect to Kafka server",
            ) from error
        except Exception as exception:
            logger.exception("Failed to start Kafka, because of %s", exception)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to start Kafka, because of {str(exception)}",
            ) from exception

    async def consume(self) -> str | None:
        """
        Consume message from Kafka topic

        :return: The decoded consumed message value, or None if error occurs
        """
        if self.consumer is None:
            logger.error("Consumer is not started.")
            return None

        try:
            async for msg in self.consumer:
                logger.info("Consumed message: %s", msg.value.decode())
                return msg.value.decode()  # type: ignore[no-any-return]
        except ConsumerStoppedError as excp:
            logger.error("Consumer has been stopped: %s", excp)
        except NoBrokersAvailable as excp:
            logger.error("No brokers available: %s", excp)
        except KafkaTimeoutError as excp:
            logger.error("Kafka operation timed out: %s", excp)
        except Exception as excp:  # pylint: disable=W0718
            logger.error("Consumer error: %s", excp)

        return None

    async def stop(self) -> None:
        """
        Consumer closing

        Finishes Kafka consumer and releases resources
        """
        if self.consumer is not None:
            await self.consumer.stop()


# Example usage
async def main() -> None:
    """
    Start code from script
    """
    producer = KafkaProducer(bootstrap_servers="localhost:9092", topic="test_topic")
    consumer = KafkaConsumer(
        bootstrap_servers="localhost:9092", topic="test_topic", group_id="my_group"
    )

    await producer.start()
    await consumer.start()

    try:
        await producer.produce_message("key", "value")
        message = await consumer.consume()
        logger.info("Consumed message: %s", message)
    except Exception as excp:  # pylint: disable=W0718
        logger.error("Error during Kafka operations: %s", excp)
    finally:
        await producer.stop()
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
