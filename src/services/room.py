import logging
from datetime import datetime
from functools import lru_cache
from uuid import UUID

from bson import ObjectId
from fastapi import WebSocket
from pydantic import ValidationError

from api.v1.auth.auth_bearer import BaseJWTBearer
from core.constant import INVITATION_EVENT_ID
from core.models import (
    ChatMessage,
    Error,
    PlayerAction,
    PlayerActionType,
    parse_message,
)
from db import models as db_models
from services.external import send_notification

jwt_bearer = BaseJWTBearer()


class RoomService:
    async def create(self, token: str, film_id: UUID, participants: list[UUID]):
        user_info = jwt_bearer.decode_jwt(token)
        new_room = db_models.Room(
            film_id=film_id,
            creator_id=user_info['id'],
            created_at=datetime.now(),
            view_progress=0,
            is_paused=True,
            participants=participants,
        )
        await new_room.insert()  # type: ignore

        await send_notification(token=token, data={'user_id': user_info['id'], 'event_id': INVITATION_EVENT_ID})

        return new_room

    async def get(self, room_id: str) -> db_models.Room | None:
        try:
            room_info = await db_models.Room.get(room_id)
            if room_info is None:
                raise Exception('Room not found')
            return room_info

        except Exception as e:
            logging.error(e)
            return None

    async def iter_json(
        self,
        websocket: WebSocket,
        room: db_models.Room,
        user_id: UUID,
    ):
        async for json_data in websocket.iter_json():
            try:
                message = parse_message(json_data)
                await self._handle_message(room, user_id, message)
                yield message
            except (ValueError, ValidationError) as e:
                await websocket.send_json(Error(message=str(e)).dict())

    async def _handle_message(
        self,
        room: db_models.Room,
        user_id: UUID,
        message: ChatMessage | PlayerAction,
    ):
        if isinstance(message, ChatMessage):
            room.messages.append(
                db_models.Message(
                    user_id=user_id,
                    created_at=datetime.now(),
                    message=message.content,
                )
            )
        elif isinstance(message, PlayerAction):
            match message.action:
                case PlayerActionType.play:
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
