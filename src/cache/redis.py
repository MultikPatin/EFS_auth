from datetime import timedelta
from logging import Logger
from typing import Any
from uuid import UUID
from redis.asyncio import Redis

from src.configs.app import settings
from src.cache.abstract import AbstractCache


class RedisCache(AbstractCache):
    _redis: Redis
    _logger: Logger

    def __init__(self, redis: Redis, logger: Logger):
        self._redis = redis
        self._logger = logger

    async def close(self) -> None:
        """
        Close the connection with Redis.
        """
        await self._redis.aclose()
        self._logger.info("Connection to Redis was closed.")

    async def ping(self) -> Any:
        """
        Ping the Redis server to ensure the connection is still alive.
        """
        return await self._redis.ping()

    async def _collect_keys(self, user_uuid: UUID) -> list[str] | None:
        """
        Collect all the user's refresh_token.

        Args:
            user_uuid (UUID): The user's UUID for searching for keys.

        Returns:
            list[str] | None: returns refresh_token if any
        """
        keys = []
        async for key in self._redis.scan_iter(f"{str(user_uuid)}:*", 10000):
            keys.append(key)
            if len(keys) == settings.token.user_max_sessions:
                break
        return keys

    @staticmethod
    def _build_key(user_uuid: UUID, token: bytes | str) -> str:
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
        return f"{str(user_uuid)}:{token}"

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
        key = self._build_key(user_uuid, token)

        try:
            await self._redis.set(
                name=key,
                value=token,
                ex=timedelta(minutes=settings.token.expire_time_in_minutes),
            )
        except Exception as error:
            self._logger.error(
                "Error setting value with key `%s::%s`: %s.",
                key,
                token,
                error,
            )
            raise

    async def get_tokens(
        self,
        user_uuid: UUID,
    ) -> list[bytes] | None:
        """
        Get tokens from the cache.

        Args:
            user_uuid (UUID): The key used for caching the tokens.

        Returns:
            The cached tokens, or None if the tokens are not in the cache.
        """
        keys = await self._collect_keys(user_uuid)

        try:
            values = await self._redis.mget(keys)
            if not values:
                return None
        except Exception as error:
            self._logger.error(
                "Error getting value with key `%s`: %s.", user_uuid, error
            )
            raise

        return values

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
        if all_tokens:
            keys = await self._collect_keys(uuid)
        else:
            keys = [self._build_key(uuid, token)]
        try:
            await self._redis.delete(*keys)
        except Exception as get_error:
            self._logger.error(
                "Error deletion value with key `%s`: %s.", keys, get_error
            )
            raise
        return


redis: RedisCache | None = None


async def get_redis() -> RedisCache | None:
    return redis
