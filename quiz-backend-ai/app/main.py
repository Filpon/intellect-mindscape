from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.configs.logging_handler import configure_logging_handler
from app.kafka.kafka_consumer import kafka_consumer
from app.routers import study_recommendations
from app.services.create_recommendations import process_game_messages
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

logger = configure_logging_handler()


scheduler = AsyncIOScheduler()


async def analyze_and_send_recommendations(application: FastAPI):
    """
    Analyzing game messages and sends recommendations

    The asynchronous function retrieves game messages from a consumer, processes them,
    and logs the response. It is intended to be called in asynchronous context
    """
    logger.info("Analyze and sending recommendations start")
    consumer = application.state.consumer
    response = await process_game_messages(consumer=consumer)
    logger.info(response)


@asynccontextmanager
async def lifespan_handler(application: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application start and shutdown handler
    """
    await kafka_consumer.start()
    application.state.consumer = kafka_consumer
    logger.info("Application client Kafka consumer was started")
    scheduler.add_job(
        analyze_and_send_recommendations,
        "interval",
        minutes=1,
        args=[application],
    )
    scheduler.start()
    logger.info("Game backend AI container was started")
    yield
    await application.state.consumer.stop()
    logger.info("Application client Kafka consumer was finished")
    logger.info("Game backend AI container shutdown")


app = FastAPI(
    docs_url="/api/v1/docs", openapi_url="/api/v1/openapi", lifespan=lifespan_handler
)
app.include_router(
    study_recommendations.router, prefix="/api/v1/kafka", tags=["recommendations"]
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8003)
