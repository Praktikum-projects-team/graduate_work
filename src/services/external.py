from uuid import UUID

from core.request import make_get_request, make_post_request
from core.routes import FRIENDS_URL, NOTIFICATIONS_ADMIN_URL, NOTIFICATIONS_SERVICE_URL


async def get_user_friends(token: str) -> list[UUID]:
    friends_resp = await make_get_request(FRIENDS_URL, token=token)
    friends_ids = [friend['id'] for friend in friends_resp.body['friends']]

    return friends_ids


async def add_notification_service(token: str, data: dict) -> None:
    await make_post_request(NOTIFICATIONS_SERVICE_URL, data=data, token=token)


# Создание события админом, которое будет использоваться при создании комнаты
# Написать скрипт с этим методом (предварительно получив токен) или накатить дамп с этим событием
async def add_notification_admin_for_room(token: str) -> None:
    data = {
        'description': 'Комната просмотра',
        'is_unsubscribe': False,
        'cron_string': '',
    }
    event_info = await make_post_request(NOTIFICATIONS_ADMIN_URL, data=data, token=token)

    return event_info.event_id
