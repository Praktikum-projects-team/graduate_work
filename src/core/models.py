from enum import Enum

from .base_model import OrjsonBaseModel


class MessageType(str, Enum):
    player = 'player'
    text = 'text'
    error = 'error'


class PlayerActionType(str, Enum):
    play = 'play'
    pause = 'pause'
    resume = 'resume'
    skip_next = 'skip_next'
    skip_previous = 'skip_previous'


class BaseMessage(OrjsonBaseModel):
    type: MessageType


class PlayerAction(BaseMessage):
    type: MessageType = MessageType.player
    action: PlayerActionType
    value: float


class ChatMessage(BaseMessage):
    type: MessageType = MessageType.text
    content: str


class Error(BaseMessage):
    type: MessageType = MessageType.error
    message: str


def parse_message(json_data: dict):
    type = json_data.get('type')
    if type == MessageType.player:
        return PlayerAction(**json_data)
    elif type == MessageType.text:
        return ChatMessage(**json_data)

    raise ValueError('Unknown message type')