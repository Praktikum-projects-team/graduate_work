import logging
from http import HTTPStatus

import pytest
import uuid

from tests.functional.testdata.users import get_users_data
from tests.functional.utils.routes import ROOM_URL
from tests.functional.utils.helpers import decode_jwt


@pytest.fixture
async def create_room(user_access_token, make_post_request):
    async def inner():
        users = get_users_data()
        users_tokens = [await user_access_token(user) for user in users]
        room_resp = await make_post_request(
            path=ROOM_URL,
            data={'film_id': str(uuid.uuid4()), 'participants': [decode_jwt(token)['id'] for token in users_tokens]},
            token=users_tokens[0]
        )

        return room_resp.body['room_id'], users_tokens[0]

    return inner



