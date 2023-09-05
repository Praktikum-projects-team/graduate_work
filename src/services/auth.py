import json
import logging
from http import HTTPStatus
from uuid import UUID, uuid4

import jwt
from fastapi import HTTPException
from httpx import AsyncClient, ConnectError

from core.config import AuthConfig, auth_config


class AuthApi:
    def __init__(self):
        self.auth_header_key = 'Authorization'
        self.token_type = 'Bearer'
        self.x_request_id = 'x_request_id'
        self.token_checking_url = AuthConfig().host + '/api/v1/auth/check_access_token'

    class AuthServiceBadStatus(Exception):
        pass

    async def check_token(self, token):
        async with AsyncClient(timeout=None) as client:
            auth_answer = await client.post(
                self.token_checking_url,
                headers={self.auth_header_key: self.token_type + ' ' + token, 'X-Request-Id': str(uuid4())},
            )
        if auth_answer.status_code == HTTPStatus.OK:
            body = auth_answer.json()
            return json.loads(body)
        if auth_answer.status_code == HTTPStatus.UNAUTHORIZED:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token or expired token.")
        else:
            raise self.AuthServiceBadStatus('auth service responded with status %s', auth_answer.status_code)

    def decode_jwt(self, token: str) -> dict | None:
        try:
            payload = jwt.decode(
                jwt=token,
                key=auth_config.jwt_secret,
                algorithms=[auth_config.jwt_algorithm],
            )
            token_payload = json.loads(payload.get('user_info'))
            return token_payload
        except jwt.PyJWTError:
            return {}

    async def get_user(self, token):
        try:
            return await self.check_token(token)
        except (ConnectError, self.AuthServiceBadStatus):
            logging.exception('auth api connection error')
            return self.decode_jwt(token)


def get_auth_api():
    return AuthApi()