from collections import defaultdict

from fastapi import WebSocket
from pydantic import BaseModel


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        self._connections[room_id].append(websocket)

    async def disconnect(self, room_id: str, websocket: WebSocket):
        if room_id not in self._connections:
            raise KeyError()

        self._connections[room_id].remove(websocket)

    async def send_message(self, room_id: str, message: BaseModel):
        if room_id not in self._connections:
            raise KeyError()

        for websocket in self._connections[room_id]:
            await websocket.send_json(message.dict())


_connection_manager = ConnectionManager()


def get_connection_manager():
    return _connection_manager
