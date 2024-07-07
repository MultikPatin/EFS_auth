from uuid import UUID

from abc import ABC, abstractmethod


class AbstractValidator(ABC):
    @abstractmethod
    async def is_exists(self, instance_uuid: UUID) -> UUID:
        raise NotImplementedError
