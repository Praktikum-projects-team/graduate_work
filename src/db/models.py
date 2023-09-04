import uuid
from datetime import datetime
from uuid import UUID

from beanie import Document
from pydantic import BaseModel, Field


class Message(BaseModel):
    user_id: UUID
    created_at: datetime
    message: str


class Room(Document):
    id: UUID = Field(default_factory=uuid.uuid4)
    film_id: UUID
    creator_id: UUID
    created_at: datetime
    view_progress: int
    is_paused: bool
    participants: list[UUID]
    messages: list[Message] = Field(default_factory=list)

    class Settings:
        name = 'rooms'
