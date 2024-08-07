from functools import lru_cache
from typing import Any
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.api.v1 import (
    RequestRoleCreate,
    RequestRoleUpdate,
)
from src.db.clients.postgres import (
    PostgresDatabase,
    get_postgres_db,
)
from src.db.entities import Role
from src.db.repositories.base import PostgresRepository


class RoleRepository(
    PostgresRepository[
        Role,
        RequestRoleCreate,
        RequestRoleUpdate,
    ],
):
    async def get_with_permissions(self, role_uuid: UUID) -> Any | None:
        async with self._database.get_session() as session:
            db_obj = await session.execute(
                select(self._model)
                .filter_by(role_uuid=role_uuid)
                .options(selectinload(Role.permissions))
            )
            return db_obj.unique().scalars().first()


@lru_cache
def get_role_repository(
    database: PostgresDatabase = Depends(get_postgres_db),
) -> RoleRepository:
    return RoleRepository(database, Role)
