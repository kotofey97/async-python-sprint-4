import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from api.v1 import base
from core import config
from core.config import app_settings
from core.logger import LOGGING
from core.middleware import BlackListMiddleware

app = FastAPI(
    # Конфигурируем название проекта. Оно будет отображаться в документации
    title=app_settings.app_title,
    # Адрес документации в красивом интерфейсе
    docs_url='/api/swagger',
    # Адрес документации в формате OpenAPI
    openapi_url='/api/swagger.json',
    # Можно сразу сделать небольшую оптимизацию сервиса 
    # и заменить стандартный JSON-сериализатор на более шуструю версию, написанную на Rust
    default_response_class=ORJSONResponse,
)

black_list= BlackListMiddleware(black_list=app_settings.black_list)

app.add_middleware(BaseHTTPMiddleware, dispatch=black_list)
app.include_router(base.router, prefix='/api/v1')

if __name__ == '__main__':
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8080`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run(
        'main:app',
        host=config.PROJECT_HOST,
        port=config.PROJECT_PORT,
    )
