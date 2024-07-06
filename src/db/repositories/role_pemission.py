from typing import Any, TypeVar
from uuid import UUID

from fastapi import Depends
from sqlalchemy import delete, select

from src.db.repositories.base import PostgresRepositoryCRD
from src.models.api.v1 import RequestRolePermissionCreate
from src.db.clients.postgres import (
    PostgresDatabase,
    get_postgres_db,
)
from src.db.entities import RolePermission, Entity

ModelType = TypeVar("ModelType", bound=Entity)


class RolePermissionRepository(
    PostgresRepositoryCRD[RolePermission, RequestRolePermissionCreate]
):
    async def remove(self, instance_uuid: UUID, **kwargs) -> UUID:
        permission_uuid = kwargs.get("permission_uuid")
        async with self._database.get_session() as session:
            await session.execute(
                delete(self._model).filter_by(
                    role_uuid=instance_uuid, permission_uuid=permission_uuid
                )
            )
            await session.commit()
        return instance_uuid

    async def get(self, instance_uuid: UUID, **kwargs) -> RolePermission | Any:
        permission_uuid = kwargs.get("permission_uuid")
        async with self._database.get_session() as session:
            db_obj = await session.execute(
                select(self._model).filter_by(
                    role_uuid=instance_uuid, permission_uuid=permission_uuid
                )
            )
            return db_obj.scalars().first()

    async def get_all(self) -> list[ModelType] | Any:
        raise NotImplementedError()


def get_role_permission_repository(
    database: PostgresDatabase = Depends(get_postgres_db),
) -> RolePermissionRepository:
    return RolePermissionRepository(database, RolePermission)
