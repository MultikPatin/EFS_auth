from fastapi import Depends

from src.db.repositories.role_pemission import (
    RolePermissionRepository,
    get_role_permission_repository,
)
from src.validators import BaseValidator, DuplicateRowValidatorMixin


class RolePermissionValidator(
    BaseValidator[RolePermissionRepository], DuplicateRowValidatorMixin
):
    pass


def get_role_permission_validator(
    repository: RolePermissionRepository = Depends(get_role_permission_repository),
) -> RolePermissionValidator:
    return RolePermissionValidator(repository)
