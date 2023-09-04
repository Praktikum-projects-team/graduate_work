import logging
from http import HTTPStatus

import pytest
import requests
import uuid

from tests.functional.testdata.users import get_users_data
from tests.functional.utils.routes import ROOM_URL


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
