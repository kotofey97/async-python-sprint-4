from typing import Any, Optional, Union

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.logger import LOGGING
from db import get_session
from schemas.urls import OriginalUrl, ShortUrl, UrlHistoryFullInfo, UrlHistoryShortInfo, OriginalUrlsList, ShortUrlsList

# from services import link_crud

# from .utils import validate_link
# Объект router, в котором регистрируем обработчики
router = APIRouter()

API_TAG_HEALTH = 'Service health'
API_TAG_URLS = 'Urls'


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=ShortUrl,
    description='Получить сокращенный вариант переданного URL.',
    tags=[API_TAG_URLS]
)
async def create_short_url(
        original_url: OriginalUrl,
        db: AsyncSession = Depends(get_session)
) -> Any:
    """Получить сокращенный вариант переданного URL"""
    # obj = await link_crud.create(db=db, obj_in=target_url)
    # logger.info(
    #     'Created short url %s for %s', obj.short_url, obj.original_url
    # )
    return 


@router.get(
    '/{url_id}',
    response_class=RedirectResponse,
    description='Вернуть оригинальный URL.',
    tags=[API_TAG_URLS],
)
async def get_url(
        url_id: str,
        request: Request,
        db: AsyncSession = Depends(get_session)
) -> Any:
    """Вернуть оригинальный URL"""
    # obj = await link_crud.get(db=db, url_id=url_id)
    # validate_link(obj=obj)
    # await link_crud.update_usage_count(db=db, db_obj=obj)
    # await link_crud.create_link_usage(
    #     db=db,
    #     link_id=obj.id,
    #     request=request
    # )
    # logger.info(
    #     'Redirect from %s to %s', obj.short_url, obj.original_url
    # )
    return # obj.original_url



@router.get(
    '/{url_id}/status',
    response_model=UrlHistoryShortInfo | UrlHistoryFullInfo,
    description="Вернуть статус использования URL",
    tags=[API_TAG_URLS],
)
async def get_url_status(
        url_id: str,
        full_info: bool | None = Query(default=None, alias='full-info'),
        max_size: int = Query(
            default=10,
            ge=1,
            alias='max-size',
            description='Query max size.'
        ),
        offset: int = Query(
            default=0,
            ge=0,
            description='Query offset.'
        ),
        db: AsyncSession = Depends(get_session),
) -> Any:
    """Вернуть статус использования URL."""
    # obj = await link_crud.get(db=db, url_id=url_id)
    # validate_link(obj=obj)
    # res = await link_crud.get_status(
    #     db=db,
    #     db_obj=obj,
    #     limit=max_size,
    #     offset=offset,
    #     full_info=full_info
    # )
    # if isinstance(res, int):
    #     logger.info('Sent short status for url_id %s', url_id)
    #     return JSONResponse(
    #         status_code=status.HTTP_200_OK,
    #         content={'usages_count': res}
    #     )
    # logger.info('Sent full status for url_id %s', url_id)
    return #res








@router.get(
    '/ping',
    # response_model=links.Ping,
    description='Возвращает информацию о статусе доступности БД.',
    tags=[API_TAG_HEALTH],
)
async def check_db(db: AsyncSession = Depends(get_session)) -> Any:
    """Возвращает информацию о статусе доступности БД"""
    # logger.info('A ping to the DB is requested')
    return #await link_crud.get_ping_db(db=db)





@router.post(
    '/shorten',
    status_code=status.HTTP_201_CREATED,
    response_model=ShortUrlsList,
    description='Массовое сокращение ссылок.',
    tags=[API_TAG_URLS],
)
async def create_short_urls(
        target_urls: OriginalUrlsList,
        db: AsyncSession = Depends(get_session)
) -> Any:
    """Массовое сокращение ссылок"""
    # logger.info('Created a batch links of short url')
    return# await link_crud.create_multi(db=db, obj_in=target_urls)


@router.get(
    '/',
    description='Версия api.',
    tags=[API_TAG_HEALTH],
)
async def api_version():
    return {'version': 'v1'}
