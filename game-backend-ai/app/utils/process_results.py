import asyncio
import json
import os
import re
from collections import defaultdict

import pandas as pd
from app.configs.logging_handler import configure_logging_handler
from app.database.repository.game import CRUDGame
from app.database.schemas import ScoredPointModel
from app.utils.keydb import keydb_instance
from dotenv import load_dotenv
from fastapi import HTTPException, status
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from qdrant_client import AsyncQdrantClient, models
from qdrant_client.http.exceptions import ResponseHandlingException
from sentence_transformers import SentenceTransformer

load_dotenv()

QDRANT_HOSTNAME = os.getenv("QDRANT_HOSTNAME")
QDRANT_PORT = os.getenv("QDRANT_PORT")
REACT_APP_DOMAIN_NAME = os.getenv("REACT_APP_DOMAIN_NAME")
SENTENCE_MODEL_IN_USE = os.getenv("SENTENCE_MODEL_IN_USE")
LARGE_LANGUAGE_MODEL_IN_USE = os.getenv("LARGE_LANGUAGE_MODEL_IN_USE")
OLLAMA_HOSTNAME = os.getenv("OLLAMA_HOSTNAME")
OLLAMA_PORT = os.getenv("OLLAMA_PORT")

logger = configure_logging_handler()


class ResultsProcessing:
    """
    Class for processing game results and generating statistics and recommendations.

    The class interacts with Qdrant for storing and retrieving game data,
    processes game results, and generates studying recommendations based on user performance
    """

    async_qdrant_client = AsyncQdrantClient(
        url=f"http://{QDRANT_HOSTNAME}{REACT_APP_DOMAIN_NAME}:{QDRANT_PORT}"
    )
    model = SentenceTransformer(SENTENCE_MODEL_IN_USE)

    @classmethod
    async def order_game_results(cls, game_results: list) -> defaultdict:
        """
        Generate organized statistics for processing game results.
        The method takes a list of game results, decodes and parses each result,
        and organizes them by game mode. It returns a defaultdict containing the
        organized results.

        :param list game_results: List of game result records, where each record
                            contains a JSON-encoded string with game data
        :return: Defaultdict where keys are game modes and values are lists
                of game data associated with each mode
        """
        organized_results = defaultdict(list)
        for record in game_results:
            value = record.value.decode("utf-8")
            data = json.loads(value)  # Parse t`he JSON string
            organized_results[data["mode"]].append(
                data
            )  # Append the data to game_results
        return organized_results

    @classmethod
    async def create_collection(cls, collection_name: str):
        """
        Creates a collection in Qdrant if it doesn't already exist

        :param str collection_name: The name of the collection to create
        """
        vector_size = 384  # Adjust this based on your model's output size
        distance_metric = (
            models.Distance.COSINE
        )  # Choose the appropriate distance metric
        try:
            is_collection_exists = await cls.async_qdrant_client.collection_exists(
                collection_name=collection_name
            )
            if not is_collection_exists:
                await cls.async_qdrant_client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(
                        size=vector_size, distance=distance_metric
                    ),
                )
                logger.info("Qdrant collection %s was created", collection_name)
        except ResponseHandlingException as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable connect to Qdrant server",
            ) from error

    @classmethod
    async def process_game_results(cls, game_results: list, collection_name: str):
        """
        Generates embeddings for game results and stores them in Qdrant

        :param list game_results: A list of organized game results
        :param str collection_name: The name of the collection to store results
        """
        # Initialize Async Qdrant client
        await cls.create_collection(collection_name=collection_name)
        # Initialize the SentenceTransformer model
        # Generate embeddings and store in Qdrant, organized by mode
        for _, questions in game_results.items():
            for question_data in questions:
                question = question_data["question"]
                logger.info("Question: %s", question)
                # Generate embedding using SentenceTransformer
                embedding = await asyncio.to_thread(
                    cls.model.encode, question
                )  # Use asyncio.to_thread for blocking call
                # Upload the embedding to Qdrant
                await cls.async_qdrant_client.upsert(
                    collection_name=collection_name,
                    points=[
                        {
                            "id": question_data[
                                "gameId"
                            ],  # Use gameId as the unique ID
                            "vector": embedding.tolist(),
                            "payload": question_data,  # Store original data as payload
                        }
                    ],
                )

    @classmethod
    async def fetch_game_data_from_qdrant(cls, collection_name: str) -> list[dict]:
        """
        Fetches game data from Qdrant

        :param str collection_name: The name of the collection to fetch data from

        :return list[dict]: List of game data records
        """
        try:
            query_vector = [0.1] * 384
            query_filter = {
                "must_not": [
                    {
                        "key": "mode",
                        "match": {
                            "value": ""  # Exclude mode equal to an empty string
                        },
                    }
                ]
            }
            results = await cls.async_qdrant_client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                query_filter=query_filter,
            )
            return results
        except ResponseHandlingException as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable connect to Qdrant server",
            ) from error

    @classmethod
    async def generate_statistics(cls, collection_name: str) -> list[dict]:
        """
        Generates statistics based on game data retrieved from Qdrant.

        :param str collection_name: The name of the collection to fetch game data from

        :return list[dict]: List of statistics grouped by user and mode
        """
        game_data = await cls.fetch_game_data_from_qdrant(
            collection_name=collection_name
        )
        user_sub_ids_dict = await CRUDGame.fetch_user_id_with_games()
        game_data_restructured = [
            ScoredPointModel(
                id=point.id,
                version=point.version,
                score=point.score,
                gameId=point.payload["gameId"],
                mode=point.payload["mode"],
                question=point.payload["question"],
                userAnswer=point.payload["userAnswer"],
                correctAnswer=point.payload["correctAnswer"],
                isCorrect=point.payload["isCorrect"],
                shard_key=point.shard_key,
                order_value=point.order_value,
            ).dict()
            for point in game_data
        ]
        df = pd.DataFrame(game_data_restructured)
        # Including user_sub_id to DataFrame
        df["user_sub_id"] = df["id"].map(user_sub_ids_dict)
        statistics = (
            df.groupby(["user_sub_id", "mode"])
            .agg(
                incorrect_answers=("isCorrect", lambda x: (x == False).sum()),
                correct_answers=("isCorrect", lambda x: (x == True).sum()),
                questions=("question", list),
            )
            .reset_index()
        )

        return statistics

    @classmethod
    async def generate_recommendations(cls, statistics: list) -> list[dict]:
        """
        Generates recommendations based on user statistics.

        :param list statistics: List of statistics grouped by user and mode

        :return list[dict]: List of recommendations for each user
        """
        llm = OllamaLLM(
            model=LARGE_LANGUAGE_MODEL_IN_USE,
            base_url=f"{OLLAMA_HOSTNAME}:{OLLAMA_PORT}",
            think=False,
        )
        recommendations = {}
        prompt = ChatPromptTemplate.from_template("""Acting like helpful valid learning assistant.
            If you can't help with this learning task, just write "I can't help with this learning task"
            Question: {question}
            Context: {context}
            """)
        question = """Please create legal appropriate learning recomendations in one-two sentences length
        basing on user context data theme - this is mode in obtaining context data,
        context data questions and context data incorrect answers."""
        for user_sub_id in statistics["user_sub_id"].unique():
            # LLM generation recommendation
            context = statistics[statistics["user_sub_id"] == user_sub_id].to_dict(
                orient="records"
            )
            recommendation_text = prompt.invoke(
                {"question": question, "context": context}
            )
            recommendation_text_result = llm.invoke(recommendation_text)
            recommendations[user_sub_id] = re.sub(
                r"<think>.*?</think>", "", recommendation_text_result, flags=re.DOTALL
            )

        # Final output report formation
        final_output = []

        for _, row in statistics.iterrows():
            recommendations_dictionary = {
                "user_sub_id": row["user_sub_id"],
                "mode": row["mode"],
                "questionVars": row["questions"],
                "modeRecomendation": recommendations[row["user_sub_id"]],
            }
            final_output.append(recommendations_dictionary)
            recommendations_dictionary["mode"] = json.dumps(row["mode"])
            recommendations_dictionary["questionVars"] = json.dumps(row["questions"])
            recommendations_dictionary["modeRecomendation"] = json.dumps(
                recommendations[row["user_sub_id"]]
            )
            keydb_instance.hmset(
                name=f"{row['user_sub_id']}-recommendations-{row['mode']}",
                mapping=recommendations_dictionary,
            )

        return final_output
