import asyncio
from uuid import uuid4

import models
import requests
from pydantic import BaseModel
from websockets.client import WebSocketClientProtocol, connect


class Token(BaseModel):
    access_token: str
    refresh_token: str


async def receive_message(websocket: WebSocketClientProtocol):
    while True:
        message = await websocket.recv()
        print(f'Received: {message}')


async def send_message(websocket: WebSocketClientProtocol):
    while True:
        model_type = await models.MessageType.cli_select()
        message = await model_type.model.cli_input()
        await websocket.send(message.json())


def create_room(token: Token) -> str:
    url = 'http://127.0.0.1:8003/api/v1/room'
    headers = {'Authorization': f'Bearer {token.access_token}'}
    payload = {'film_id': str(uuid4()), 'participants': []}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f'Create room failed, {response.text}')
    return response.json().get('room_id')


def get_token(email: str, password: str):
    url = 'http://127.0.0.1:8000/api/v1/auth/login'
    headers = {'X-Request-Id': str(uuid4())}
    payload = {'login': email, 'password': password}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f'Login failed, {response.text}')
    return Token(**response.json())


async def main():
    email = input('Enter your email:\n')
    password = input('Enter your password:\n')

    token = get_token(email, password)
    room_id = input('Enter room id or empty for creating new room:\n')
    if room_id == '':
        room_id = create_room(token)
        print(f'Room {room_id} created')

    url = f'ws://127.0.0.1/api/v1/room/{room_id}?token={token.access_token}'
    async with connect(url) as websocket:
        await asyncio.gather(
            receive_message(websocket),
            send_message(websocket),
        )


if __name__ == '__main__':
    asyncio.run(main())
