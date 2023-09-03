import json

import pytest
import websockets

from asyncio import sleep

from functional.testdata.users import get_users_data
from functional.utils.routes import ROOM_URL

pytestmark = pytest.mark.asyncio


class TestWS:
    async def test_chat_messages(self, create_room):
        room_id = await create_room()
        room_url = f'{ROOM_URL}/{room_id}'
        ws1 = await websockets.connect(room_url)
        ws2 = await websockets.connect(room_url)
        ws3 = await websockets.connect(room_url)
        message = {'type': 'text', 'content': "Всем привет!"}
        await ws1.send(json.dumps(message))
        msg_rsv_2 = await ws2.recv()
        msg_rsv_3 = await ws2.recv()

        assert message == msg_rsv_2, 'Wrong message'
        assert message == msg_rsv_3, 'Wrong message'

    async def test_player_messages(self, create_room):
        room_id = await create_room()
        room_url = f'{ROOM_URL}/{room_id}'
        ws1 = await websockets.connect(room_url)
        ws2 = await websockets.connect(room_url)
        ws3 = await websockets.connect(room_url)
        message = {'type': 'player', 'action': 'play', 'value': 1}
        await ws2.send(json.dumps(message))
        msg_rsv_1 = await ws1.recv()
        msg_rsv_3 = await ws3.recv()

        assert message == msg_rsv_1, 'Wrong message'
        assert message == msg_rsv_3, 'Wrong message'



