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
from db.models import Message
from services.external import send_notification

jwt_bearer = BaseJWTBearer()


class RoomService:

    class RoomInvitationNotSent(Exception):
        pass

    async def create(self, user: dict, film_id: UUID, participants: list[UUID], token: str = None):
        new_room = db_models.Room(
            film_id=film_id,
            creator_id=user['id'],
            created_at=datetime.now(),
            view_progress=0,
            is_paused=True,
            participants=participants,
        )
        await new_room.insert()  # type: ignore

        try:
            await send_notification(token=token, data={'user_id': user['id'], 'event_id': INVITATION_EVENT_ID})
        except ConnectionError:
            logging.error('room %s invitations not sent', new_room.id)

        return new_room

    async def get(self, room_id: str) -> db_models.Room | None:
        return await db_models.Room.get(room_id)

    async def update(self, room_id: str, field: str, value: list | bool | int):
        try:
            room_info = await db_models.Room.get(room_id)
            if room_info is None:
                raise Exception('Room not found')

            setattr(room_info, field, value)
            await room_info.replace()  # type: ignore
            
            return room_info

        except Exception as e:
            logging.error(e)

            return None

    async def update_messages(self, token: str, room_id: str, message_info: dict):
        user_info = jwt_bearer.decode_jwt(token)
        message_info.update({'user_id': user_info['id'], 'created_at': datetime.now()})

        room_info = await self.update(room_id=room_id, field='messages', value=[Message(**message_info)])

        return room_info

    async def update_is_paused(self, room_id: str, is_paused: bool):
        room_info = await self.update(room_id=room_id, field='is_paused', value=is_paused)

        return room_info

    async def update_view_progress(self, room_id: str, view_progress: int):
        room_info = await self.update(room_id=room_id, field='view_progress', value=view_progress)

        return room_info

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
