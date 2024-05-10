from typing import Generic, TypeVar

from pydantic import BaseModel

from src.content.db.abstract import AbstractDBClient
from src.content.models.api.v1.role import ResponsePermission
from src.core.cache.abstract import AbstractModelCache

ModelDB = TypeVar("ModelDB", bound=BaseModel)


class BaseElasticService(Generic[ModelDB]):
    _key_prefix: str
    _index: str

    def __init__(
        self,
        cache: AbstractModelCache,
        cache_ex: int,
        db: AbstractDBClient,
    ):
        self._cache = cache
        self._db = db
        self._cache_ex = cache_ex

    async def _get_by_id(
        self,
        obj_id: str,
        model: type[ModelDB],
        user_permissions: list[ResponsePermission],
    ) -> ModelDB | None:
        key_user_permissions = None
        if user_permissions:
            key_user_permissions = "".join(
                [permission.name for permission in user_permissions]
            )
        key = self._cache.build_key(
            self._key_prefix, obj_id, key_user_permissions
        )
        doc = await self._cache.get_one_model(key, model)
        if not doc:
            doc = await self._db.get_by_id(
                obj_id=obj_id, model=model, index=self._index
            )
            if not doc:
                return None
            await self._cache.set_one_model(key, doc, self._cache_ex)
        return doc

    async def _get_search(
        self,
        page_number: int,
        page_size: int,
        search_query: str | None,
        field: str,
        model: type[ModelDB],
        user_permissions: list[ResponsePermission],
    ) -> list[ModelDB] | None:
        key_user_permissions = None
        if user_permissions:
            key_user_permissions = "".join(
                [permission.name for permission in user_permissions]
            )
        key = self._cache.build_key(
            self._key_prefix,
            page_number,
            page_size,
            search_query,
            key_user_permissions,
        )
        persons = await self._cache.get_list_model(key, model)
        if not persons:
            persons = await self._db.get_search_by_query(
                page_number=page_number,
                page_size=page_size,
                field=field,
                query=search_query,
                model=model,
                index=self._index,
            )
            if not persons:
                return None
            await self._cache.set_list_model(key, persons, self._cache_ex)
        return persons
