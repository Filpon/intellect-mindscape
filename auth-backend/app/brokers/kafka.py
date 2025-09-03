import asyncio
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from app.configs.logging_handler import configure_logging_handler

logger = configure_logging_handler()


class KafkaProducer:
    """
    Kafka producer for sending messages to a specified topic
    """

    def __init__(self, bootstrap_servers: str, topic: str):
        """
        Initializes kafka producer instance

        :param str bootstrap_servers: The Kafka server bootstrap address
        :param str topic: The topic to which messages will be sent
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = None

    async def start(self):
        """
        Start the Kafka producer

        Initializes the AIOKafkaProducer and connects to the Kafka server.
        """
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await self.producer.start()

    async def produce_message(self, key, value):
        """
        Produce a message to the Kafka topic

        :param key: The key for the message
        :param value: The value of the message
        """
        try:
            await self.producer.send_and_wait(
                self.topic, key=key.encode(), value=value.encode()
            )
            logger.info("Message delivered to %s", self.topic)
        except Exception as e:
            logger.error("Message delivery failed: %s", e)

    async def close(self):
        """
        Close the producer
        """
        await self.producer.stop()


class KafkaConsumer:
    """
    Kafka consumer for consuming messages from specified topic
    """

    def __init__(self, bootstrap_servers: str, topic: str, group_id: str):
        """
        Initializes Kafka Consumer and connects to the Kafka server

        :param str bootstrap_servers: The Kafka server address
        :param str topic: The topic from which messages will be consumed
        :param str group_id: The consumer group ID
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer = None

    async def start(self):
        """
        Start Kafka consumer
        """
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset="earliest",
        )
        await self.consumer.start()

    async def consume(self):
        """
        Consume message from Kafka topic

        :return: The decoded consumed message value, or None if error occurs
        """
        try:
            async for msg in self.consumer:
                logger.info("Consumed message: %s", msg.value.decode())
                return msg.value.decode()
        except Exception as e:
            logger.error("Consumer error: %s", e)
            return None

    async def close(self):
        """
        Consumer closing

        Finishes Kafka consumer and releases resources
        """
        await self.consumer.stop()


# Example usage
async def main():
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
    except Exception as e:
        logger.error("Error during Kafka operations: %s", e)
    finally:
        await producer.close()
        await consumer.close()


if __name__ == "__main__":
    asyncio.run(main())
