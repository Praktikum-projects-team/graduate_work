import json
from http import HTTPStatus
from typing import Any
import jwt
from pydantic import BaseModel

from tests.functional.settings import test_settings


class ApiResponse(BaseModel):
    status: HTTPStatus
    body: Any


def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, test_settings.jwt_secret, algorithms=[test_settings.jwt_algorithm])
        return json.loads(payload.get('user_info'))
    except jwt.PyJWTError:
        return {}
