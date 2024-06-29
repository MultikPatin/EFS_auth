from functools import lru_cache

from fastapi import Depends

from src.models.api.v1.permissions import (
    RequestPermissionCreate,
    RequestPermissionUpdate,
)
from src.auth.db.clients.postgres import (
    PostgresDatabase,
    get_postgres_auth_db,
)
from src.auth.db.entities import Permission
from src.auth.db.repositories.base import (
    CountRepositoryMixin,
    NameFieldRepositoryMixin,
    PostgresRepository,
)


class PermissionRepository(
    PostgresRepository[
        PostgresDatabase,
        Permission,
        RequestPermissionCreate,
        RequestPermissionUpdate,
    ],
    NameFieldRepositoryMixin,
    CountRepositoryMixin,
):
    pass


@lru_cache
def get_permission_repository(
    database: PostgresDatabase = Depends(get_postgres_auth_db),
) -> PermissionRepository:
    return PermissionRepository(database, Permission)
