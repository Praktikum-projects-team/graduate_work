import pytest
import uuid
from http import HTTPStatus

from tests.functional.testdata.users import get_users_data
from tests.functional.utils.routes import ROOM_URL

pytestmark = pytest.mark.asyncio
