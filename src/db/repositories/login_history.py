from functools import lru_cache
from typing import Sequence, TypeVar
from uuid import UUID

from fastapi import Depends
from sqlalchemy import func, select

from src.db.repositories.base import PostgresRepositoryCRD
from src.models.api.v1 import RequestLoginHistory
from src.db.clients.postgres import (
    PostgresDatabase,
    get_postgres_db,
)
from src.db.entities import LoginHistory, Entity

ModelType = TypeVar("ModelType", bound=Entity)


class LoginHistoryRepository(PostgresRepositoryCRD[LoginHistory, RequestLoginHistory]):
    async def remove(self, instance_uuid: UUID, **kwargs) -> UUID:
        raise NotImplementedError

    async def get_by_user(self, user_uuid: UUID, **kwargs) -> Sequence[ModelType]:
        limit = kwargs.get("limit")
        offset = kwargs.get("offset")
        async with self._database.get_session() as session:
            query = (
                select(self._model)
                .filter_by(user_uuid=user_uuid)
                .order_by(self._model.created_at.desc())
            )
            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
            db_obj = await session.execute(query)
            return db_obj.scalars().all()

    async def count(self, **kwargs) -> int | None:
        async with self._database.get_session() as session:
            db_obj = await session.execute(
                select(func.count()).select_from(self._model).filter_by(**kwargs)
            )
            return db_obj.scalars().first()


@lru_cache
def get_login_history_repository(
    database: PostgresDatabase = Depends(get_postgres_db),
) -> LoginHistoryRepository:
    return LoginHistoryRepository(database, LoginHistory)
