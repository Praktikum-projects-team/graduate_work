from datetime import datetime
from uuid import UUID

from beanie import Document
from pydantic import BaseModel, Field


class Message(BaseModel):
    user_id: UUID
    created_at: datetime
    message: str


class Room(Document):
    film_id: UUID
    creator_id: UUID
    created_at: datetime
    view_progress: float
    is_paused: bool
    participants: list[UUID]
    messgess: list[Message] = Field(default_factory=list)

    class Settings:
        name = 'rooms'
