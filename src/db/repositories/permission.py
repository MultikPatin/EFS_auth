from functools import lru_cache

from fastapi import Depends

from src.models.api.v1.permissions import (
    RequestPermissionCreate,
    RequestPermissionUpdate,
)
from src.db.clients.postgres import (
    PostgresDatabase,
    get_postgres_db,
)
from src.db.entities import Permission
from src.db.repositories.base import PostgresRepository


class PermissionRepository(
    PostgresRepository[
        Permission,
        RequestPermissionCreate,
        RequestPermissionUpdate,
    ],
):
    pass


@lru_cache
def get_permission_repository(
    database: PostgresDatabase = Depends(get_postgres_db),
) -> PermissionRepository:
    return PermissionRepository(database, Permission)
