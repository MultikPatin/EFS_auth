from typing import TypeVar, Generic
from uuid import UUID

from fastapi import HTTPException

from src.db.repositories.abstract import AbstractRepository
from src.validators.abstract import AbstractValidator

Repository = TypeVar("Repository", bound=AbstractRepository)


class InitValidator:
    def __init__(self, repository: Repository):
        self._repository: Repository = repository


class BaseValidator(InitValidator, AbstractValidator, Generic[Repository]):
    async def is_exists(self, instance_uuid: UUID) -> UUID:
        instance = await self._repository.get(instance_uuid)
        if instance is None:
            raise HTTPException(
                status_code=404,
                detail=f"The object with uuid='{instance_uuid}' was not found",
            )
        return instance_uuid


class DuplicateNameValidatorMixin(InitValidator):
    async def is_duplicate_name(self, name: str) -> None:
        permission_uuid = await self._repository.get_uuid_filter_by(name=name)
        if permission_uuid is not None:
            raise HTTPException(
                status_code=400,
                detail=f"The object with name='{name}'already exists",
            )


class DuplicateEmailValidatorMixin(InitValidator):
    async def is_duplicate_email(self, email: str) -> None:
        user_uuid = await self._repository.get_uuid_filter_by(email=email)
        if user_uuid is not None:
            raise HTTPException(
                status_code=400,
                detail=f"The object with email='{email}'already exists",
            )


class DuplicateRowValidatorMixin(InitValidator):
    async def is_duplicate_row(self, role_uuid: UUID, permission_uuid: UUID) -> None:
        permission_uuid = await self._repository.get(
            role_uuid, permission_uuid=permission_uuid
        )
        if permission_uuid is not None:
            raise HTTPException(
                status_code=400,
                detail=f"The row with role_uuid='{role_uuid}' and"
                f"permission_uuid='{permission_uuid}' already exists",
            )
