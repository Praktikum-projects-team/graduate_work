import json
import uuid

import pytest
import websockets

from tests.functional.settings import test_settings
from tests.functional.utils.routes import ROOM_URL

pytestmark = pytest.mark.asyncio


class TestWS:
    async def test_chat_messages(self, create_room):
        room_id, token = await create_room()
        room_url = f'ws://{test_settings.api_host}:{test_settings.api_port}{ROOM_URL}/{room_id}?token={token}'

        message = {'type': 'text', 'content': "Всем привет!"}
        ws = await websockets.connect(room_url)
        await ws.send(json.dumps(message))
        msg_rsv = await ws.recv()

        assert message == json.loads(msg_rsv), 'Wrong message'

    async def test_player_messages(self, create_room):
        room_id, token = await create_room()
        room_url = f'ws://{test_settings.api_host}:{test_settings.api_port}{ROOM_URL}/{room_id}?token={token}'
        ws = await websockets.connect(room_url)
        message = {'type': 'player', 'action': 'play', 'value': 1}
        await ws.send(json.dumps(message))
        msg_rsv = await ws.recv()

        assert message == json.loads(msg_rsv), 'Wrong message'



