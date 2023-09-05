from enum import Enum

import aioconsole
from pydantic import BaseModel


class MessageType(str, Enum):
    player = 'player'
    text = 'text'
    error = 'error'

    @property
    def model(self) -> type['BaseMessage']:
        match self:
            case MessageType.player:
                return PlayerAction
            case MessageType.text:
                return ChatMessage
            case MessageType.error:
                return Error

    @classmethod
    async def cli_select(cls):
        question = 'Choose a message type:'
        for i, message_type in enumerate(cls):
            question += f'\n{i+1}. {message_type}'

        selected_idx = int(await aioconsole.ainput(question + '\n')) - 1
        if selected_idx < 0 or selected_idx >= len(cls):
            raise ValueError('Invalid number')

        return [message_type for message_type in cls][selected_idx]


class PlayerActionType(str, Enum):
    play = 'play'
    pause = 'pause'
    skip_next = 'skip_next'
    skip_previous = 'skip_previous'

    @classmethod
    async def cli_select(cls):
        question = 'Choose a player action type:'
        for i, message_type in enumerate(cls):
            question += f'\n{i+1}. {message_type}'

        selected_idx = int(await aioconsole.ainput(question + '\n')) - 1
        if selected_idx < 0 or selected_idx >= len(cls):
            raise ValueError('Invalid number')

        return [message_type for message_type in cls][selected_idx]


class BaseMessage(BaseModel):
    type: MessageType

    @classmethod
    async def cli_input(cls) -> 'BaseMessage':
        raise NotImplementedError


class PlayerAction(BaseMessage):
    type: MessageType = MessageType.player
    action: PlayerActionType
    value: int

    @classmethod
    async def cli_input(cls):
        return cls(
            action=await PlayerActionType.cli_select(),
            value=await aioconsole.ainput('Enter a value:\n'),
        )


class ChatMessage(BaseMessage):
    type: MessageType = MessageType.text
    content: str

    @classmethod
    async def cli_input(cls):
        return cls(content=await aioconsole.ainput('Enter a content:\n'))


class Error(BaseMessage):
    type: MessageType = MessageType.error
    message: str

    @classmethod
    async def cli_input(cls):
        return cls(message=await aioconsole.ainput('Enter an error message:\n'))
