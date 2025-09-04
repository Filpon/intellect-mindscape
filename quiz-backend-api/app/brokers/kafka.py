import asyncio

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from app.configs.logging_handler import configure_logging_handler

logger = configure_logging_handler()


class KafkaProducer:
    def __init__(self, bootstrap_servers: str, topic: str):
        """
        Initialize the KafkaProducer instance

        :param str bootstrap_servers: Kafka connecting server
        :param str topic: Kafka topic name
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = None

    async def start(self):
        """
        Creation active Kafka producer

        """
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await self.producer.start()

    async def produce_message(self, key, value):
        """
        Produce message to Kafka topic

        :param str key: The Kafka key for message sending
        :param str value: The value for sending
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
    def __init__(self, bootstrap_servers: str, topic: str, group_id: str):
        """
        Initialize the KafkaConsumer instance

        :param str bootstrap_servers: Kafka connecting server
        :param str topic: Kafka topic name
        :param str group_id: Kafka group_id
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer = None

    async def start(self):
        """
        Creation active Kafka consumer

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
        Consume Kafka messages

        """
        try:
            async for msg in self.consumer:
                logger.info("Consumed message: %s", msg.value.decode())
                return msg.value.decode()
        except Exception as e:
            logger.error("Consumer error: %s", e)
            return None

    async def close(self):
        await self.consumer.stop()


# Example usage
async def main():
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
