from sqlalchemy import Column, Integer, String, Enum, Float, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.config.database import Base
from enum import Enum as PyEnum

class StatusEnum(str, PyEnum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    path: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum), server_default=StatusEnum.pending, nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, server_default="0", nullable=False)
    is_blurry: Mapped[bool] = mapped_column(Boolean, nullable=True)
    sharpness_score: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,)
    failed_reason: Mapped[str | None] = mapped_column(String(200), nullable=True)
    next_attempt_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True,)
    started_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True,)