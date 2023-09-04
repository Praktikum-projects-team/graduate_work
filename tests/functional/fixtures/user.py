import logging
from http import HTTPStatus

import pytest
import requests

from tests.functional.testdata.users import get_users_data
from tests.functional.utils.routes import AUTH_URL_LOGIN, AUTH_URL_SIGN_UP
from tests.functional.testdata.users import get_users_data, UserData


@pytest.fixture(scope="session", autouse=True)
async def create_users_default():
    for user in get_users_data():
        requests.post('http://auth:8000/api/v1/auth/sign_up', headers={"X-Request-Id": "1"}, json={
            'login': user.login,
            'password': user.password,
            'name': user.name
        })
    logging.info("Users successfully created")


@pytest.fixture
async def user_access_token():
    async def inner(user: UserData):
        resp = requests.post(
            AUTH_URL_LOGIN,
            headers={"X-Request-Id": "1"},
            json={
                'login': user.login,
                'password': user.password
            }
        )
        if resp.status_code != HTTPStatus.OK:
            raise Exception(resp.text)

        resp_data = resp.json()

        return resp_data['access_token']

    return inner
