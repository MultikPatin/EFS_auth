from functools import lru_cache

from fastapi import Depends

from src.models.api.v1.permissions import (
    RequestPermissionCreate,
    RequestPermissionUpdate,
    ResponsePermissionsPaginated,
)
from src.models.db.permission import PermissionDB
from src.services.base import BaseService
from src.db.repositories.permission import (
    PermissionRepository,
    get_permission_repository,
)


class PermissionService(
    BaseService[
        PermissionDB,
        ResponsePermissionsPaginated,
        RequestPermissionCreate,
        RequestPermissionUpdate,
    ]
):
    pass


@lru_cache
def get_permission_service(
    repository: PermissionRepository = Depends(get_permission_repository),
) -> PermissionService:
    return PermissionService(repository, PermissionDB)
