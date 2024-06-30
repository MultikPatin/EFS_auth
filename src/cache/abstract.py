from abc import ABC, abstractmethod
from uuid import UUID


class AbstractCache(ABC):
    @abstractmethod
    async def set_token(
        self,
        user_uuid: UUID,
        token: str | bytes,
    ) -> None:
        """
        Set token in the cache.

        Args:
            user_uuid (UUID): The key to use for caching the token.
            token(str | bytes): str: The token.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_tokens(self, user_uuid: UUID) -> list[bytes] | None:
        """
        Get tokens from the cache.

        Args:
            user_uuid (UUID): The key used for caching the tokens.

        Returns:
            The cached tokens, or None if the tokens are not in the cache.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_tokens(
        self, uuid: UUID, token: bytes | str, all_tokens: bool = False
    ) -> None:
        """
        Delete tokens from the cache.

        Args:
            uuid (UUID): The pattern used for search the tokens to delete; key prefix.
            token (bytes | str): The parameter to build key to delete.
            all_tokens (bool) The parameter to switch between single and multiply deletion.

        """
        raise NotImplementedError
