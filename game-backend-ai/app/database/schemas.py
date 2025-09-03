from pydantic import BaseModel

# Define the Pydantic model
class ScoredPointModel(BaseModel):
    """
    :param int id: Unique identifier for the scored point
    :param int version: Version number of the scored point model
    :param float score: The score associated with the point
    :param int gameId: Identifier for the game to which the point belongs
    :param str mode: The mode of the game (e.g. music, arithmetic, trigonometry)
    :param str question: The question associated with the scored point
    :param str userAnswer: The answer provided by the user
    :param str correctAnswer: The correct answer for the question
    :param bool isCorrect: Indicates whether the user's answer is correct
    :param str | None shard_key: Optional key for sharding the data
    :param str | None order_value: Optional value for ordering the scored points
    """
    id: int
    version: int
    score: float
    gameId: int
    mode: str
    question: str
    userAnswer: str
    correctAnswer: str
    isCorrect: bool
    shard_key: str | None = None
    order_value: str | None = None
