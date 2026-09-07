from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime
from app.models.jobs import StatusEnum

class CreateJob(BaseModel):
    path: str = Field(min_length=2, max_length=200, description="Path of the image to be processed")
    model_config = ConfigDict(extra="forbid")



class JobItems(BaseModel):
    id: int
    path: str
    status: StatusEnum
    attempts: int
    is_blurry: bool | None
    sharpness_score: float | None
    created_at: datetime
    updated_at: datetime | None
    failed_reason: str | None = None
    next_attempt_at: datetime | None = None
    started_at: datetime | None = None

class JobGetResponse(BaseModel):
    next_cursor: int | None = None
    avail_next: bool
    result: list[JobItems]