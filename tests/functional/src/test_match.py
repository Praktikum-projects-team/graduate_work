import pytest
import uuid
from http import HTTPStatus

from tests.functional.testdata.users import get_users_data
from tests.functional.utils.routes import MATCHES_URL
from tests.functional.utils.helpers import decode_jwt

pytestmark = pytest.mark.asyncio


class TestMatches:
    async def test_matches(self, make_get_request_with_token, user_access_token,
                           create_friend, create_bookmark, delete_bookmark):
        users = get_users_data()
        users_tokens = [await user_access_token(user) for user in users]
        film_id1 = str(uuid.uuid4())
        film_id2 = str(uuid.uuid4())
        film_id3 = str(uuid.uuid4())

        await create_friend(decode_jwt(users_tokens[0])['id'], decode_jwt(users_tokens[1])['id'], users_tokens[0])
        await create_friend(decode_jwt(users_tokens[0])['id'], decode_jwt(users_tokens[2])['id'], users_tokens[0])

        for token in users_tokens:
            await create_bookmark(token, film_id1)
            await create_bookmark(token, film_id2)

        await create_bookmark(users_tokens[0], film_id3)
        await create_bookmark(users_tokens[1], film_id3)

        resp = await make_get_request_with_token(path=MATCHES_URL, token=users_tokens[0])

        for token in users_tokens:
            await delete_bookmark(token, film_id1)
            await delete_bookmark(token, film_id2)

        await delete_bookmark(users_tokens[0], film_id3)
        await delete_bookmark(users_tokens[1], film_id3)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert len(resp.body[film_id1]) == 2, 'Wrong response'
        assert len(resp.body[film_id2]) == 2, 'Wrong response'
        assert len(resp.body[film_id3]) == 1, 'Wrong response'
