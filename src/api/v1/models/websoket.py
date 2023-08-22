from enum import Enum

from core.base_model import OrjsonBaseModel


class MessageType(str, Enum):
    player = 'player'
    text = 'text'


class PlayerAction(str, Enum):
    skip = 'skip'
    play = 'play'
    pause = 'pause'
    resume = 'resume'
    skip_next = 'skip_next'
    skip_previous = 'skip_previous'


class BaseMessage(OrjsonBaseModel):
    type: MessageType


class BasePlayerAction(BaseMessage):
    type: MessageType = MessageType.player
    action: PlayerAction
    value: float


class ChatMessage(BaseMessage):
    type: MessageType = MessageType.text
    content: str
