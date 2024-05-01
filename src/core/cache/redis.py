from logging import Logger
from typing import Any

from redis.asyncio import Redis


class RedisBase:
    __redis: Redis
    __logger: Logger

    def __init__(self, redis: Redis, logger: Logger):
        self.__redis = redis
        self.__logger = logger

    async def close(self) -> None:
        """
        Закрыть соединение с Redis.
        """
        await self.__redis.aclose()
        self.__logger.info("Connection to Redis was closed.")

    async def ping(self) -> Any:
        """
        Ping the Redis server to ensure the connection is still alive.
        """
        return await self.__redis.ping()
