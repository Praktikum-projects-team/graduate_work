import os

from pydantic import BaseSettings, Field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestSettings(BaseSettings):
    api_host: str = Field(..., env='APP_HOST')
    auth_host: str = Field(..., env='AUTH_HOST')

    # Для локального запуска тестов
    class Config:
        env_file = os.path.join(BASE_DIR, '.env')


test_settings = TestSettings()
