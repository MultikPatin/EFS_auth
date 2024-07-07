import logging

from datetime import timedelta
from typing import Any
from redis.asyncio import Redis

from src.configs import TokenSettings
from src.cache.abstract import AbstractCache

logger = logging.getLogger("RedisCache")


class RedisCache(AbstractCache):
    def __init__(self, cache: Redis, settings: TokenSettings):
        self.__cache = cache
        self.__settings = settings

    async def close(self) -> None:
        """
        Close the connection with Redis.
        """
        await self.__cache.aclose()
        logger.info("Connection to Redis was closed.")

    async def ping(self) -> Any:
        """
        Ping the Redis server to ensure the connection is still alive.
        """
        return await self.__cache.ping()

    async def __collect_keys(self, user_uuid: str) -> list[str] | None:
        """
        Collect all the user's refresh_token.

        Args:
            user_uuid (str): The user's UUID for searching for keys.

        Returns:
            list[str] | None: returns refresh_token if any
        """
        keys = []
        async for key in self.__cache.scan_iter(f"{user_uuid}:*", 10000):
            keys.append(key)
            if len(keys) == self.__settings.user_max_sessions:
                break
        return keys

    @staticmethod
    def _build_key(user_uuid: str, token: bytes | str) -> str:
        """
        Build a key for a specific user based on their UUID and a token.

        Args:
            user_uuid (str): The UUID of the user.
            token (bytes|str): The token to be used in the key generation.
                It can be either a string or a bytes object.

        Returns:
            The built cache key.
        """
        if isinstance(token, bytes):
            token = str(token, encoding="utf-8")
        return f"{user_uuid}:{token}"

    async def set_token(
        self,
        user_uuid: str,
        token: str | bytes,
    ) -> None:
        """
        Set token in the cache.

        Args:
            user_uuid (UUID): The key to use for caching the token.
            token(str | bytes): str: The token.
        """
        key = self._build_key(user_uuid, token)

        try:
            await self.__cache.set(
                name=key,
                value=token,
                ex=timedelta(minutes=self.__settings.expire_time_in_minutes),
            )
        except Exception as error:
            logger.error(
                "Error setting value with key `%s::%s`: %s.",
                key,
                token,
                error,
            )
            raise

    async def get_tokens(
        self,
        user_uuid: str,
    ) -> list[bytes] | None:
        """
        Get tokens from the cache.

        Args:
            user_uuid (UUID): The key used for caching the tokens.

        Returns:
            The cached tokens, or None if the tokens are not in the cache.
        """
        keys = await self.__collect_keys(user_uuid)

        try:
            values = await self.__cache.mget(keys)
            if not values:
                return None
        except Exception as error:
            logger.error("Error getting value with key `%s`: %s.", user_uuid, error)
            raise

        return values

    async def delete_tokens(
        self, user_uuid: str, token: bytes | str, all_tokens: bool = False
    ) -> None:
        """
        Delete tokens from the cache.

        Args:
            user_uuid (str): The pattern used for search the tokens to delete; key prefix.
            token (bytes | str): The parameter to build key to delete.
            all_tokens (bool) The parameter to switch between single and multiply deletion.

        """
        if all_tokens:
            keys = await self.__collect_keys(user_uuid)
        else:
            keys = [self._build_key(user_uuid, token)]
        try:
            await self.__cache.delete(*keys)
        except Exception as get_error:
            logger.error("Error deletion value with key `%s`: %s.", keys, get_error)
            raise
        return


redis: RedisCache | None = None


async def get_redis() -> RedisCache | None:
    return redis
