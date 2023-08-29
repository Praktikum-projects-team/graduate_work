from datetime import datetime
from functools import lru_cache
from uuid import UUID

from core.models import ChatMessage, PlayerAction, PlayerActionType
from db import models as db_models


class RoomService:
    async def create(self, user_id: UUID, film_id: UUID):
        new_room = db_models.Room(
            film_id=film_id,
            creator_id=user_id,
            created_at=datetime.now(),
            view_progress=0.0,
            is_paused=True,
            participants=[user_id],
        )
        await new_room.insert()  # type: ignore
        return new_room

    async def get(self, room_id: str):
        return await db_models.Room.get(room_id)

    async def handle_message(
        self,
        room: db_models.Room,
        user_id: UUID,
        message: ChatMessage | PlayerAction,
    ):
        if isinstance(message, ChatMessage):
            room.messgess.append(
                db_models.Message(
                    user_id=user_id,
                    created_at=datetime.now(),
                    message=message.content,
                )
            )
        elif isinstance(message, PlayerAction):
            match message.action:
                case PlayerActionType.play | PlayerActionType.resume:
                    room.is_paused = False
                case PlayerActionType.pause:
                    room.is_paused = True
                case PlayerActionType.skip_next:
                    room.view_progress += message.value
                case PlayerActionType.skip_previous:
                    room.view_progress -= message.value

        await room.save()  # type: ignore


@lru_cache
def get_room_service():
    return RoomService()
