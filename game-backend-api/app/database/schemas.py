from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.database.models import GameStatus


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class GameRequest(BaseModel):
    user_sub_id: UUID
    latency_seconds: int
    mode: str


class GameResponse(BaseModel):
    id: int
    user_sub_id: UUID
    status: GameStatus
    mode_name: str  # Updated to match the ForeignKey in Game model
    correct_score: int = 0
    incorrect_score: int = 0
    total_score: int = 0


class GameResult(BaseModel):
    id: int
    status: GameStatus
    finished_at: datetime
    correct_score: int
    incorrect_score: int
    total_score: int

    class Config:
        orm_mode = True  # This allows compatibility with ORM models if needed


class GameScoreResult(BaseModel):
    correct_score: int
    incorrect_score: int

    class Config:
        orm_mode = True  # This allows compatibility with ORM models if needed


class QuestionRequest(BaseModel):
    user_token: str
    mode: str
    difficulty: str


class QuestionResponse(BaseModel):
    question: str
    options: List[str]
    time_limit: int


class StatsRequest(BaseModel):
    user_token: str


class StatsResponse(BaseModel):
    total_games: int
    correct_answers: int
    incorrect_answers: int
    answered_questions_collected: Optional[
        List[dict]
    ]  # Added to reflect the JSON field in AnswersDetails
