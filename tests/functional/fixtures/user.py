import logging
from http import HTTPStatus

import pytest
import requests

from tests.functional.utils.routes import AUTH_URL_LOGIN, FRIENDS_URL, BOOKMARK_URL
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


@pytest.fixture
async def create_friend():
    async def inner(user_id: str, friend_id: str, token: str):
        resp = requests.post(
            FRIENDS_URL,
            headers={'Authorization': f'Bearer {token}'},
            json={
                'user_id': user_id,
                'friend_id': friend_id
            }
        )
        if resp.status_code not in [HTTPStatus.OK, HTTPStatus.CONFLICT]:
            raise Exception(resp.text)

        return resp.json()

    return inner


@pytest.fixture
async def get_friends():
    async def inner(token: str):
        resp = requests.get(
            FRIENDS_URL,
            headers={'Authorization': f'Bearer {token}'}
        )
        if resp.status_code != HTTPStatus.OK:
            raise Exception(resp.text)

        return resp.json()

    return inner


@pytest.fixture
async def delete_friend():
    async def inner(friend_id: str, token: str):
        resp = requests.delete(
            f'{FRIENDS_URL}/{friend_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        if resp.status_code != HTTPStatus.OK:
            raise Exception(resp.text)

        return resp.json()

    return inner


@pytest.fixture
async def create_bookmark():
    async def inner(token: str, film_id: str):
        resp = requests.post(
            BOOKMARK_URL,
            headers={'Authorization': f'Bearer {token}'},
            json={
                'film_id': film_id
            }
        )
        if resp.status_code != HTTPStatus.OK:
            raise Exception(resp.text)

        return resp.json()

    return inner


@pytest.fixture
async def delete_bookmark():
    async def inner(token: str, film_id: str):
        resp = requests.delete(
            BOOKMARK_URL,
            headers={'Authorization': f'Bearer {token}'},
            json={
                'film_id': film_id
            }
        )
        if resp.status_code != HTTPStatus.OK:
            raise Exception(resp.text)

        return resp.json()

    return inner
