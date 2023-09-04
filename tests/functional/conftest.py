import uuid

import pytest
import asyncio

from functional.testdata.users import get_users_data
from functional.utils.routes import ROOM_URL

pytest_plugins = ('tests.functional.fixtures.user', 'tests.functional.fixtures.request')


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def create_room(user_access_token, make_post_request):
    users = get_users_data()
    token = await user_access_token(users[0])
    room_resp = await make_post_request(
        path=ROOM_URL,
        data={'film_id': str(uuid.uuid4()), 'participants': [str(user.id) for user in users]},
        token=token
    )
    return room_resp.body.room_id
