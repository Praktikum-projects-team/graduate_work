from enum import Enum
from http import HTTPStatus
from typing import Any

from pydantic import BaseModel

from .base_model import OrjsonBaseModel


class ApiResponse(BaseModel):
    status: HTTPStatus
    body: Any


class MessageType(str, Enum):
    player = 'player'
    text = 'text'
    error = 'error'


class PlayerActionType(str, Enum):
    play = 'play'
    pause = 'pause'
    skip_next = 'skip_next'
    skip_previous = 'skip_previous'


class BaseMessage(OrjsonBaseModel):
    type: MessageType


class PlayerAction(BaseMessage):
    type: MessageType = MessageType.player
    action: PlayerActionType
    value: int


class ChatMessage(BaseMessage):
    type: MessageType = MessageType.text
    content: str


class Error(BaseMessage):
    type: MessageType = MessageType.error
    message: str


def parse_message(json_data: dict):
    type = json_data.get('type')
    match type:
        case MessageType.player:
            return PlayerAction(**json_data)
        case MessageType.text:
            return ChatMessage(**json_data)
        case _:
            raise ValueError('Unknown message type')
