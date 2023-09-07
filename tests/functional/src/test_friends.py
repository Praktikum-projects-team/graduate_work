import pytest
from http import HTTPStatus

from tests.functional.testdata.users import get_users_data
from tests.functional.utils.helpers import decode_jwt

pytestmark = pytest.mark.asyncio


class TestFriends:
    async def test_getting_friends(self, user_access_token, create_friend, get_friends):
        users = get_users_data()
        users_tokens = [await user_access_token(user) for user in users]
        await create_friend(decode_jwt(users_tokens[0])['id'], decode_jwt(users_tokens[1])['id'], users_tokens[0])
        await create_friend(decode_jwt(users_tokens[0])['id'], decode_jwt(users_tokens[2])['id'], users_tokens[0])

        resp = await get_friends(token=users_tokens[0])

        assert len(resp['friends']) == 2, 'Wrong result'

    async def test_del_friends(self, user_access_token, create_friend, delete_friend, get_friends):
        users = get_users_data()
        users_tokens = [await user_access_token(user) for user in users]
        await create_friend(decode_jwt(users_tokens[0])['id'], decode_jwt(users_tokens[1])['id'], users_tokens[0])
        await create_friend(decode_jwt(users_tokens[0])['id'], decode_jwt(users_tokens[2])['id'], users_tokens[0])

        resp = await delete_friend(friend_id=decode_jwt(users_tokens[1])['id'], token=users_tokens[0])
        get_resp = await get_friends(token=users_tokens[0])

        assert len(get_resp['friends']) == 1, 'Wrong result'



