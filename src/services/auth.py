import json
from http import HTTPStatus

from fastapi import HTTPException
from httpx import AsyncClient

from core.config import AuthConfig


class AuthApi:
    def __init__(self):
        self.auth_header_key = 'Authorization'
        self.token_type = 'Bearer'
        self.x_request_id = 'x_request_id'
        self.token_checking_url = AuthConfig().host + '/api/v1/auth/check_access_token'

    async def check_token(self, token):
        async with AsyncClient() as client:
            auth_answer = await client.post(
                self.token_checking_url,
                headers={self.auth_header_key: self.token_type + ' ' + token, 'X-Request-Id': self.x_request_id},
            )
        if auth_answer.status_code == HTTPStatus.OK:
            body = auth_answer.json()
            return json.loads(body)
        if auth_answer.status_code == HTTPStatus.UNAUTHORIZED:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token or expired token.")


def get_auth_api():
    return AuthApi()
