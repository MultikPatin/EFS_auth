from typing import Generic, Any
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, func, select

from src.db.clients.postgres import PostgresDatabase
from src.db.repositories.abstract import (
    AbstractRepository,
    ModelType,
    CreateSchemaType,
    UpdateSchemaType,
)


class InitRepository:
    def __init__(self, database: PostgresDatabase, model: type[ModelType]):
        self._database = database
        self._model = model


class PostgresRepository(
    InitRepository,
    AbstractRepository,
    Generic[ModelType, CreateSchemaType, UpdateSchemaType],
):
    async def create(self, instance: CreateSchemaType) -> ModelType:
        async with self._database.get_session() as session:
            db_obj = self._model(**instance.dict())
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def get_all(self) -> list[ModelType] | Any:
        async with self._database.get_session() as session:
            db_objs = await session.execute(select(self._model))
            return db_objs.scalars().all()

    async def get(self, instance_uuid: UUID, **kwargs) -> ModelType | Any:
        async with self._database.get_session() as session:
            db_obj = await session.execute(
                select(self._model).where(self._model.uuid == instance_uuid)
            )
            return db_obj.scalars().first()

    async def update(
        self, instance_uuid: UUID, instance: UpdateSchemaType
    ) -> ModelType:
        async with self._database.get_session() as session:
            db_obj = await self.get(instance_uuid)

            obj_data = jsonable_encoder(db_obj)
            update_data = instance.dict(exclude_unset=True)

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def remove(self, instance_uuid: UUID) -> UUID:
        async with self._database.get_session() as session:
            await session.execute(
                delete(self._model).where(self._model.uuid == instance_uuid)
            )
            await session.commit()
            return instance_uuid

    async def count(self) -> int | None:
        async with self._database.get_session() as session:
            db_obj = await session.execute(
                select(func.count()).select_from(self._model)
            )
            return db_obj.scalars().first()

    async def get_uuid_filter_by(self, filter_by: dict[str, Any]) -> str | None:
        if not filter_by:
            raise ValueError("Filter by is empty")
        async with self._database.get_session() as session:
            db_obj = await session.execute(
                select(self._model.uuid).filter_by(**filter_by)
            )
            obj_uuid = db_obj.scalars().first()
            return obj_uuid


# class NameFieldRepositoryMixin(InitRepository):
#     async def get_uuid_by_name(self, name: str) -> UUID | None:
#         async with self._database.get_session() as session:
#             db_obj = await session.execute(
#                 select(self._model.uuid).filter_by(**{"name": name})
#             )
#             obj_uuid = db_obj.scalars().first()
#             return obj_uuid
#
#
# class EmailFieldRepositoryMixin(InitRepository):
#     async def get_uuid_by_email(self, email: str) -> UUID | None:
#         async with self._database.get_session() as session:
#             db_obj = await session.execute(
#                 select(self._model.uuid).filter_by(**{"email": email})
#             )
#             obj_uuid = db_obj.scalars().first()
#             return obj_uuid
#
#     async def get_by_email(self, email: str) -> ModelType | None:
#         async with self._database.get_session() as session:
#             db_obj = await session.execute(
#                 select(self._model).filter_by(**{"email": email})
#             )
#             return db_obj.scalars().first()
