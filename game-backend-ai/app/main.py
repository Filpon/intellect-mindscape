from app.configs.logging_handler import configure_logging_handler
from app.kafka.kafka_consumer import kafka_consumer
from app.routers import study_recommendations
from app.services.create_recommendations import process_game_messages
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

logger = configure_logging_handler()

app = FastAPI(docs_url="/api/v1/docs", openapi_url="/api/v1/openapi")
app.include_router(study_recommendations.router, prefix="/api/v1/kafka", tags=["recommendations"])

scheduler = AsyncIOScheduler()


async def analyze_and_send_recommendations():
    """
    Analyzing game messages and sends recommendations

    This asynchronous function retrieves game messages from a consumer, processes them, 
    and logs the response. It is intended to be called in asynchronous context
    """
    logger.info("Analyze and sending recommendations start")
    consumer = app.state.consumer
    response = await process_game_messages(consumer=consumer)
    logger.info(response)


@app.on_event("startup")
async def startup_event():
    """
    Starting application
    """
    await kafka_consumer.start()
    app.state.consumer = kafka_consumer
    scheduler.add_job(
        analyze_and_send_recommendations, "interval", minutes=15
    )
    scheduler.start()

    logger.info("Game backend AI container was started")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutting down
    """
    logger.info("Game backend AI container shutdown")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8003)
