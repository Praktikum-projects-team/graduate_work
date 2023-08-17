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


class PostgresConfig(BaseSettings):
    host: str = Field(..., env='POSTGRES_HOST')
    port: int = Field(..., env='POSTGRES_PORT')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    name: str = Field(..., env='POSTGRES_DB')

    @property
    def url_sync(self):
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'

    @property
    def url_async(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


class RabbitMQConfig(BaseSettings):
    rm_host: str = Field(..., env='RABBITMQ_HOST')
    rm_port: int = Field(..., env='RABBITMQ_PORT')
    rm_user: str = Field(..., env='RABBITMQ_DEFAULT_USER')
    rm_password: str = Field(..., env='RABBITMQ_DEFAULT_PASS')
    rm_delivery_mode: int = Field(..., env='RABBITMQ_DELIVERY_MODE')
    rm_exchange: str = Field(..., env='RABBITMQ_EXCHANGE')
    rm_instant_queue_name: str = Field(..., env='RABBITMQ_INSTANT_QUEUE')
    rm_ordinary_queue_name: str = Field(..., env='RABBITMQ_ORDINARY_QUEUE')

    @property
    def rabbit_connection(self):
        return f"amqp://{self.rm_user}:{self.rm_password}@{self.rm_host}/"


app_config = AppConfig()  # type: ignore[call-arg]
auth_config = AuthConfig()  # type: ignore[call-arg]
pg_config = PostgresConfig()  # type: ignore[call-arg]
rm_config = RabbitMQConfig()  # type: ignore[call-arg]
