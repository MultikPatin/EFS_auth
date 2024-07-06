from abc import ABC, abstractmethod
from typing import TypeVar, Any
from uuid import UUID

M = TypeVar("M")


class AbstractRepositoryCD(ABC):
    @abstractmethod
    async def create(self, instance: M) -> M:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, instance: M) -> None:
        raise NotImplementedError


class AbstractRepositoryCRD(AbstractRepositoryCD, ABC):
    @abstractmethod
    async def get_all(self) -> list[M] | Any:
        raise NotImplementedError

    @abstractmethod
    async def get(self, instance_id: UUID, **kwargs) -> M | Any:
        raise NotImplementedError


class AbstractRepository(AbstractRepositoryCRD, ABC):
    @abstractmethod
    async def update(self, instance_id: UUID, instance: M) -> M:
        raise NotImplementedError

    @abstractmethod
    async def count(self) -> int:
        raise NotImplementedError
