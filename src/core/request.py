import uuid
import aiohttp

from core.models import ApiResponse


async def make_get_request(url: str, query_data: dict = None, token: str = None):
    headers = {'X-Request-Id': str(uuid.uuid4())}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=query_data, headers=headers) as response:
            resp = ApiResponse(status=response.status, body=await response.json())

    return resp


async def make_post_request(url: str, data: dict = None, token: str = None):
    headers = {'X-Request-Id': str(uuid.uuid4())}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            resp = ApiResponse(status=response.status, body=await response.json())
    return resp
