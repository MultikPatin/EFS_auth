from functools import lru_cache

from fastapi import Depends

from src.models.api.v1 import (
    RequestRoleCreate,
    RequestRoleUpdate,
    ResponseRolesPaginated,
)
from src.models.db import RoleDB
from src.services.base import BaseService
from src.db.repositories.role import RoleRepository, get_role_repository


class RoleService(
    BaseService[
        RoleDB,
        ResponseRolesPaginated,
        RequestRoleCreate,
        RequestRoleUpdate,
    ]
):
    pass


@lru_cache
def get_role_service(
    repository: RoleRepository = Depends(get_role_repository),
) -> RoleService:
    return RoleService(repository, RoleDB)
