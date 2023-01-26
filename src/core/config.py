import os
from logging import config as logging_config
from pydantic import BaseSettings, PostgresDsn
from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'library')
PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8000'))

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class AppSettings(BaseSettings):
    app_title: str = "UrlShortenerApp"
    database_dsn: PostgresDsn = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'
    project_host: str = '0.0.0.0'
    project_port: int = 8000
    short_url_len: int = 10
    # black_list: list[str] = [
    #     '192.168.1.106'
    # ]

    class Config:
        env_file = '.env'

app_settings = AppSettings()
