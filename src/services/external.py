from uuid import UUID

from core.request import make_get_request, make_post_request
from core.routes import FRIENDS_URL, NOTIFICATIONS_URL


async def get_user_friends(token: str) -> list[UUID]:
    friends_resp = await make_get_request(FRIENDS_URL, token=token)
    friends_ids = [friend['id'] for friend in friends_resp.body['friends']]

    return friends_ids


async def add_notification(token: str, data: dict) -> None:
    await make_post_request(NOTIFICATIONS_URL, data=data, token=token)
