import json

import jwt

from core.config import auth_config


def decode_jwt(token: str):
    try:
        payload = jwt.decode(
            jwt=token,
            key=auth_config.jwt_secret,
            algorithms=[auth_config.jwt_algorithm],
        )
        return json.loads(payload.get('user_info'))
    except jwt.PyJWTError:
        raise 
