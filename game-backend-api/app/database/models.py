from datetime import datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy import (
    Enum as SqlEnum,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from app.database.db import Base


class GameStatus(str, PyEnum):
    in_progress = "in_progress"
    failed = "failed"
    completed = "completed"


class MathOperations(str, PyEnum):
    addition = "+"
    subtraction = "-"
    multiplication = "*"
    division = "/"


class GameModes(Base):
    __tablename__ = "game_modes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    user_sub_id = Column(PG_UUID(as_uuid=True), nullable=False)
    status = Column(
        SqlEnum(GameStatus), nullable=False
    )  # e.g., "in_progress", "completed"
    mode_name = Column(String, ForeignKey("game_modes.name"))
    latency_seconds = Column(Integer, default=180)
    started_at = Column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    finished_at = Column(TIMESTAMP(timezone=True), nullable=True)
    correct_score = Column(Integer, default=0)
    incorrect_score = Column(Integer, default=0)
    total_score = Column(Integer, default=0)
    mode = relationship("GameModes")
    stats = relationship(
        "Stats", back_populates="game"
    )  # Updated to reference Stats correctly


class QuestionTypes(Base):
    __tablename__ = "question_types"

    id = Column(Integer, primary_key=True, index=True)
    mode_id = Column(Integer, ForeignKey("game_modes.id"), nullable=False)
    expression_type = Column(
        String, index=True
    )  # e.g., "addition", "subtraction", "bass", "treble"
    expression_name = Column(String, index=True)  # e.g., "C", "D", "E", etc.
    expression_difficulty = Column(Integer, default=0)  # 1 or 2
    pitch = Column(String, nullable=True)  # Optional for music types
    mode = relationship("GameModes")


class Stats(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True, index=True)
    answered_questions_collected = Column(JSON)
    game_id = Column(Integer, ForeignKey("games.id"))  # ForeignKey to link to Game
    game = relationship("Game", back_populates="stats")  # Link to Game


class TrainingRecommendation(Base):
    __tablename__ = "training_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    question_type_id = Column(Integer, ForeignKey("question_types.id"), nullable=False)
    recommendation_text = Column(String)  # Textual recommendation for training
    question_type = relationship("QuestionTypes")  # Link to QuestionTypes


class ExcellentRecommendation(Base):
    __tablename__ = "excellent_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    question_type_id = Column(Integer, ForeignKey("question_types.id"), nullable=False)
    recommendation_text = Column(String)  # Textual recommendation for excellence
    question_type = relationship("QuestionTypes")  # Link to QuestionTypes
