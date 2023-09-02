from core.config import friends_config, notification_config

FRIENDS_SERVICE = f'http://{friends_config.host}:{friends_config.port}'
NOTIFICATIONS_SERVICE = f'http://{notification_config.host}:{notification_config.port}'


BASE_URL = 'api/v1'

FRIENDS_URL = f'{FRIENDS_SERVICE}/{BASE_URL}/friends'
NOTIFICATIONS_URL = f'{NOTIFICATIONS_SERVICE}/{BASE_URL}/notification/service'
