from datetime import datetime

from pydantic import BaseModel, HttpUrl


class OriginalUrl(BaseModel):
    """Изначальный урл"""
    original_url: HttpUrl

    class Config:
        orm_mode = True


class ShortUrl(BaseModel):
    """Укороченый урл"""
    url_id: str
    short_url: HttpUrl

    class Config:
        orm_mode = True


class UrlHistoryShortInfo(BaseModel):
    """Колличесво переходов"""
    usages_count: int

    class Config:
        orm_mode = True


class UrlHistoryFullInfo(BaseModel):
    """Подробная история переходов"""
    usages_count: int
    use_at: datetime
    client: str

    class Config:
        orm_mode = True


class OriginalUrlsList(BaseModel):
    """Пачка урлов"""
    __root__: list[OriginalUrl]


class ShortUrlsList(BaseModel):
    """Пачка сокращенных урлов"""
    __root__: list[ShortUrl]