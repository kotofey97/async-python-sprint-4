from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from db.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
BulkCreateSchemaType = TypeVar("BulkCreateSchemaType", bound=BaseModel)


def create_obj(data, nodel):
    pass

class Repository:

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def create_history(self, *args, **kwargs):
        raise NotImplementedError

    def get_status(self, *args, **kwargs):
        raise NotImplementedError

    def bulk_create(self, *args, **kwargs):
        raise NotImplementedError

    def ping(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType, UpdateSchemaType, BulkCreateSchemaType]):
    def __init__(self, model: Type[ModelType], request: Type[ModelType]):
        self._model = model
        self._request_model = request

    async def get(self, db: AsyncSession, url_id: Any) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.url_id == url_id)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = create_obj(obj_in_data, self._model)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_history(self, db: AsyncSession, url_id: int, client: str) -> None:
        request_obj = self._request_model(url=url_id, client=client)
        db.add(request_obj)
        await db.commit()
        await db.refresh(request_obj)

    async def get_status(
            self,
            db: AsyncSession,
            db_obj: ModelType,
            limit: int,
            offset: int,
            full_info: Optional[bool],
    ) -> Union[int, list[ModelType]]:
        if not full_info:
            return db_obj.usages_count
        statement = select(
            self._request_model
        ).where(
            self._request_model.url == db_obj.id
        ).offset(offset).limit(limit)
        res = await db.execute(statement=statement)
        return res.scalars().all()

    async def bulk_create(
            self,
            db: AsyncSession,
            obj_in: BulkCreateSchemaType
    ) -> list[ModelType]:
        list_data = jsonable_encoder(obj_in)
        db_obj = [create_obj(data, self._model) for data in list_data]
        db.add_all(db_obj)
        await db.commit()
        for obj in db_obj:
            await db.refresh(obj)
        return db_obj

    async def ping_db(self, db: AsyncSession) -> dict[str, float]:
        pass

    async def update_usage_count(self, db: AsyncSession, db_obj: ModelType) -> None:
        db_obj.usages_count += 1
        await db.commit()
        await db.refresh(db_obj)
