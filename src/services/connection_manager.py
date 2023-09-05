from collections import defaultdict
from functools import lru_cache

from fastapi import WebSocket
from pydantic import BaseModel


class ConnectionManager:
    class RoomConnectionNotFound(Exception):
        pass

    def __init__(self) -> None:
        self._connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        self._connections[room_id].append(websocket)

    async def disconnect(self, room_id: str, websocket: WebSocket):
        try:
            self._connections[room_id].remove(websocket)
        except (KeyError, ValueError) as e:
            raise self.RoomConnectionNotFound() from e

    async def send_message(self, room_id: str, message: BaseModel):
        try:
            for websocket in self._connections[room_id]:
                await websocket.send_json(message.dict())
        except KeyError as e:
            raise self.RoomConnectionNotFound() from e


@lru_cache
def get_connection_manager():
    return ConnectionManager()
