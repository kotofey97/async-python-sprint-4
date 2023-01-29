import os
from logging import config as logging_config

from pydantic import BaseSettings, PostgresDsn

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


PROJECT_NAME = os.getenv('PROJECT_NAME', 'UrlShortenerApp')
PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8000'))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHORT_URL_LEN = 8


class AppSettings(BaseSettings):
    app_title: str = PROJECT_NAME
    database_dsn: PostgresDsn = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'
    project_host: str = PROJECT_HOST
    project_port: int = PROJECT_PORT
    black_list: list[str] = [
        # '172.18.0.1',
    ]

    class Config:
        env_file = '.env'


app_settings = AppSettings()
