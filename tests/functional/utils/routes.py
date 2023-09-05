from tests.functional.settings import test_settings

AUTH_URL_SIGN_UP = f'{test_settings.auth_host}/api/v1/auth/sign_up'
AUTH_URL_LOGIN = f'{test_settings.auth_host}/api/v1/auth/login'

ROOM_URL = f'/api/v1/room'

FRIENDS_URL = f'http://{test_settings.friends_host}:{test_settings.friends_port}/api/v1/friends'

BOOKMARK_URL = f'{test_settings.ugc_host}/api/v1/bookmarks'

MATCHES_URL = '/api/v1/viewing/movie_matches'
