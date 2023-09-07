import pytest
from http import HTTPStatus

from tests.functional.utils.routes import ROOM_URL

pytestmark = pytest.mark.asyncio


class TestRoom:
    async def test_room_getting(self, create_room, make_get_request_with_token):
        room_id, token = await create_room()
        resp = await make_get_request_with_token(path=f'{ROOM_URL}/{room_id}', token=token)

        assert resp.body['id'] == room_id

