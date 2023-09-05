import os

from pydantic import BaseSettings, Field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestSettings(BaseSettings):
    api_host: str = Field(..., env='API_HOST')
    api_port: str = Field(..., env='API_PORT')
    auth_host: str = Field(..., env='AUTH_HOST')
    jwt_secret: str = Field(..., env='JWT_SECRET')
    jwt_algorithm: str = Field(..., env='JWT_ALGORITHM')
    friends_host: str = Field(..., env='FRIENDS_HOST')
    friends_port: int = Field(..., env='FRIENDS_PORT')
    ugc_host: str = Field(..., env='UGC_HOST')

    # Для локального запуска тестов
    class Config:
        env_file = os.path.join(BASE_DIR, '.env')


test_settings = TestSettings()
