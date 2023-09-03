from http import HTTPStatus
from typing import Any

from pydantic import BaseModel


class ApiResponse(BaseModel):
    status: HTTPStatus
    body: Any