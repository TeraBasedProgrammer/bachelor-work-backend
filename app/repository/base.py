from itertools import chain
from typing import Any, Iterable, Type

from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from app.core.database import Base


class BaseRepository:
    model: Any = None

    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    def unpack(self, collection: Iterable) -> list:
        return list(chain.from_iterable(collection))

    async def create(self, model_data: Type[BaseModel]) -> Type[Base]:
        new_instance = self.model(**model_data.model_dump())
        self.async_session.add(new_instance)

        await self.async_session.commit()
        return new_instance

    async def does_entity_exist(self, query: Select) -> bool:
        query = query.with_only_columns(self.model.id)
        response = await self.async_session.execute(query)

        result = response.first()
        return bool(result)

    async def exists_by_id(self, instance_id: int) -> bool:
        query = select(self.model).where(self.model.id == instance_id)
        return await self.does_entity_exist(query)

    async def get_many(self, query: Select) -> list[Any]:
        response = await self.async_session.execute(query)
        result = self.unpack(response.unique().all())
        return result

    async def get_instance(self, query: Select) -> Base:
        response = await self.async_session.execute(query)
        result = response.unique().scalar_one_or_none()
        return result

    async def update(self, instance_id: int, model_data: Type[BaseModel]) -> Type[Base]:
        query = (
            update(self.model)
            .where(self.model.id == instance_id)
            .values(
                {
                    key: value
                    for key, value in model_data.model_dump().items()
                    if value is not None
                }
            )
            .returning(self.model)
        )
        res = await self.async_session.execute(query)
        await self.async_session.commit()
        return res.unique().scalar_one()

    async def delete(self, instance_id: int) -> int:
        query = (
            delete(self.model)
            .where(self.model.id == instance_id)
            .returning(self.model.id)
        )

        result = (await self.async_session.execute(query)).scalar_one()
        await self.async_session.commit()
        return result

    async def save(self, obj: Any):
        self.async_session.add(obj)
        await self.async_session.commit()

    async def save_many(self, objects: list[Any], with_expire: bool = False):
        self.async_session.add_all(objects)
        await self.async_session.commit()
        if with_expire:
            self.async_session.expire_all()

    async def refresh(self, obj: Any, attribute_names: list[str] | None = None):
        await self.async_session.refresh(obj, attribute_names)
