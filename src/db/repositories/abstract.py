from abc import ABC, abstractmethod
from typing import TypeVar, Any
from uuid import UUID

from pydantic import BaseModel
from src.db.entities import Entity

ModelType = TypeVar("ModelType", bound=Entity)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class AbstractRepositoryCD(ABC):
    @abstractmethod
    async def create(self, instance: CreateSchemaType) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, instance_uuid: UUID) -> UUID:
        raise NotImplementedError


class AbstractRepositoryCRD(AbstractRepositoryCD, ABC):
    @abstractmethod
    async def get_all(self) -> list[ModelType] | Any:
        raise NotImplementedError

    @abstractmethod
    async def get(self, instance_uuid: UUID, **kwargs) -> ModelType | Any:
        raise NotImplementedError


class AbstractRepository(AbstractRepositoryCRD, ABC):
    @abstractmethod
    async def update(
        self, instance_uuid: UUID, instance: UpdateSchemaType
    ) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def count(self) -> int | None:
        raise NotImplementedError

    @abstractmethod
    async def get_uuid_filter_by(self, **kwargs) -> str | None:
        raise NotImplementedError
