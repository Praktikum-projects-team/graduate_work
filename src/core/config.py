import os
import datetime

from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppConfig(BaseSettings):
    base_dir: str = BASE_DIR
    project_name: str = Field(..., env='PROJECT_NAME')
    host: str = Field(..., env='APP_HOST')
    port: int = Field(..., env='APP_PORT')
    is_debug: bool = Field(..., env='IS_DEBUG')


class AuthConfig(BaseSettings):
    host: str = Field(..., env='AUTH_HOST')
    jwt_secret: str = Field(..., env='JWT_SECRET')
    jwt_algorithm: str = Field(..., env='JWT_ALGORITHM')
    JWT_SECRET_KEY: str = Field(..., env='JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES: datetime.timedelta = Field(..., env='ACCESS_TOKEN_TTL_IN_MINUTES')
    JWT_REFRESH_TOKEN_EXPIRES: datetime.timedelta = Field(..., env='REFRESH_TOKEN_TTL_IN_DAYS')
    admin_login: str = Field(..., env='AUTH_ADMIN_LOGIN')
    admin_password: str = Field(..., env='AUTH_ADMIN_PASSWORD')

    @property
    def url_verify(self):
        return f'{self.host}/api/v1/user/email_verification'

    @property
    def url_redirect(self):
        return f'{self.host}/api/v1/user/profile'


class MongoConfig(BaseSettings):
    host: str = Field(..., env='MONGO_HOST')
    port: int = Field(..., env='MONGO_PORT')
    db_name: str = Field(..., env='MONGO_DB_NAME')
    mongo_url: str = Field(..., env='MONGO_URL')


class FriendsConfig(BaseSettings):
    host: str = Field(..., env='FRIENDS_HOST')
    port: int = Field(..., env='FRIENDS_PORT')


class NotificationConfig(BaseSettings):
    host: str = Field(..., env='NOTIFICATION_HOST')
    port: int = Field(..., env='NOTIFICATION_PORT')


app_config = AppConfig()  # type: ignore[call-arg]
auth_config = AuthConfig()  # type: ignore[call-arg]
mongo_config = MongoConfig()  # type: ignore[call-arg]
friends_config = FriendsConfig()  # type: ignore[call-arg]
notification_config = NotificationConfig()  # type: ignore[call-arg]
