import aiohttp
import pytest
from tests.functional.settings import test_settings
from tests.functional.utils.helpers import ApiResponse
from aiohttp import ClientSession


@pytest.fixture(scope='session')
async def aiohttp_session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest.fixture
async def make_get_request(aiohttp_session):
    async def inner(path: str, query_data: dict = None):
        url = f'http://{test_settings.api_host}:{test_settings.api_port}' + path
        async with aiohttp_session.get(url, params=query_data) as response:
            resp = ApiResponse(status=response.status, body=await response.json())
        return resp

    return inner


@pytest.fixture
async def make_get_request_with_token(aiohttp_session):
    async def inner(path: str, query_data: dict = None, token: str = None):
        url = f'http://{test_settings.api_host}:{test_settings.api_port}' + path
        headers = {'Authorization': f'Bearer {token}'}
        async with aiohttp_session.get(url, params=query_data, headers=headers) as response:
            resp = ApiResponse(status=response.status, body=await response.json())
        return resp

    return inner


@pytest.fixture
async def make_post_request(aiohttp_session: ClientSession):
    async def inner(path: str, data: dict = None, token: str = None):
        url = f'http://{test_settings.api_host}:{test_settings.api_port}' + path
        headers = {'Authorization': f'Bearer {token}', 'X-Request-Id': '1'}
        async with aiohttp_session.post(url, json=data, headers=headers) as response:
            resp = ApiResponse(status=response.status, body=await response.json())
        return resp

    return inner


@pytest.fixture
async def make_put_request(aiohttp_session):
    async def inner(path: str, data: dict = None, token: str = None):
        url = f'http://{test_settings.api_host}:{test_settings.api_port}' + path
        headers = {'Authorization': f'Bearer {token}'}
        async with aiohttp_session.put(url, json=data, headers=headers) as response:
            resp = ApiResponse(status=response.status, body=await response.json())
        return resp

    return inner


@pytest.fixture
async def make_delete_request(aiohttp_session):
    async def inner(path: str, data: dict = None, token: str = None):
        url = f'http://{test_settings.api_host}:{test_settings.api_port}' + path
        headers = {'Authorization': f'Bearer {token}'}
        async with aiohttp_session.delete(url, json=data, headers=headers) as response:
            resp = ApiResponse(status=response.status, body=await response.json())
        return resp

    return inner
