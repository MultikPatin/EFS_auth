from typing import Any

from src.core.cache.abstract import AbstractBaseModel, AbstractModelCache
from src.core.cache.redis import RedisBase


class RedisCache(AbstractModelCache, RedisBase):
    """
    Клиент для работы с Redis.

    Args:
        redis (Redis): объект для работы с Redis
        logger (Logger): объект для записи в журналы
    """

    async def set_one_model(
        self,
        key: str,
        value: AbstractBaseModel,
        cache_expire: int,
    ) -> None:
        """
        Записать одну модель в кэш Redis.

        Args:
            key (str): ключ для записи модели
            value (AbstractBaseModel): модель для записи
            cache_expire (int): время жизни кэша в секундах

        """
        data = value.model_dump_json()
        try:
            await self._redis.set(key, data, cache_expire)
        except Exception as set_error:
            self._logger.error(
                "Error setting value with key `%s::%s`: %s.",
                key,
                value,
                set_error,
            )
            raise

    async def get_one_model(
        self, key: str, model: type[AbstractBaseModel]
    ) -> AbstractBaseModel | None:
        """
        Получить одну модель из кэша Redis.

        Args:
            key (str): ключ для получения модели
            model (AbstractBaseModel): модель для десериализации

        Returns:
            AbstractBaseModel | None: возвращает одну модель или None, если модель не найдена

        """
        try:
            value = await self._redis.get(key)
            if not value:
                return None
        except Exception as get_error:
            self._logger.error(
                "Error getting value with key `%s`: %s.", key, get_error
            )
            raise
        data = model.model_validate_json(value)
        return data

    async def set_list_model(
        self,
        key: str,
        values: list[AbstractBaseModel],
        cache_expire: int,
    ) -> None:
        """
        Записать список моделей в кэш Redis.

        Args:
            key (str): ключ для записи списка моделей
            values (list[AbstractBaseModel]): список моделей для записи
            cache_expire (int): время жизни кэша в секундах

        """
        try:
            for value in values:
                await self._redis.lpush(key, value.model_dump_json())  # type: ignore
            await self._redis.expire(key, cache_expire)
        except Exception as set_error:
            self._logger.error(
                "Error setting values with key `%s::%s`: %s.",
                key,
                values,
                set_error,
            )
            raise

    async def get_list_model(
        self, key: str, model: type[AbstractBaseModel]
    ) -> list[AbstractBaseModel] | None:
        """
        Получить список моделей из кэша Redis.

        Args:
            key (str): ключ для получения списка моделей
            model (AbstractBaseModel): модель для десериализации

        Returns:
            list[AbstractBaseModel] | None: возвращает список моделей или None, если список не найден

        """
        try:
            list_count = await self._redis.llen(key)  # type: ignore
            values = await self._redis.lrange(key, 0, list_count)  # type: ignore
            values.reverse()
            if not values:
                return None
        except Exception as get_error:
            self._logger.error(
                "Error getting values with key `%s`: %s.", key, get_error
            )
            raise
        data = []
        for value in values:
            data.append(model.model_validate_json(value))
        return data

    def build_key(self, key_prefix: str, *args: Any) -> str:
        """
        Создать ключ для кэша Redis.

        Args:
            key_prefix (str): префикс ключа
            *args: аргументы для создания ключа

        Returns:
            str: созданный ключ

        """
        if not key_prefix:
            self._logger.error("Key prefix value is required")
            raise
        key = ""
        for arg in args:
            key += f"{str(arg)}:"
        if not key:
            self._logger.error("key value is required")
            raise
        return f"{key_prefix}-{key}"


redis: RedisCache | None = None


async def get_redis() -> RedisCache | None:
    return redis
