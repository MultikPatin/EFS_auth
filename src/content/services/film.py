from functools import lru_cache
from http import HTTPStatus

from fastapi import Depends, HTTPException

from src.content.cache.redis import RedisCache, get_redis
from src.content.core.config import settings
from src.content.db.elastic import ElasticDB, get_elastic
from src.content.models.api.v1.role import ResponsePermission
from src.content.models.db.film import FilmDB
from src.content.services.base import BaseElasticService


class FilmService(BaseElasticService[FilmDB]):
    _key_prefix = "FilmService"
    _index = "movies"

    async def get_by_id(
        self, film_id: str, user_permissions: list[ResponsePermission] | None
    ) -> FilmDB | None:
        film = await self._get_by_id(
            obj_id=film_id,
            model=FilmDB,
            user_permissions=user_permissions,
        )
        if film and user_permissions:
            user_permissions_set = {
                permission.name for permission in user_permissions
            }
            film_permissions_set = (
                {permission.get("name") for permission in film.permissions}
                if film.permissions
                else set()
            )
            if not film_permissions_set.issubset(user_permissions_set):
                user_permissions = None
        if not user_permissions:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Not enough permissions to view.",
            )
        return film

    async def get_films(
        self,
        page_number: int,
        page_size: int,
        genre_uuid: str | None,
        sort: str | None,
        user_permissions: list[ResponsePermission] | None,
    ) -> list[FilmDB] | None:
        key_user_permissions = None
        if user_permissions:
            key_user_permissions = "".join(
                [permission.name for permission in user_permissions]
            )
        key = self._cache.build_key(
            self._key_prefix,
            page_number,
            page_size,
            genre_uuid,
            sort,
            key_user_permissions,
        )
        films = await self._cache.get_list_model(key, FilmDB)
        if not films:
            films = await self.__get_films_from_elastic(
                page_number, page_size, genre_uuid, sort
            )
            if not films:
                return None
            await self._cache.set_list_model(key, films, self._cache_ex)

        return await self.__get_allowed_films(films, user_permissions)

    async def get_search(
        self,
        page_number: int,
        page_size: int,
        search_query: str | None,
        field: str,
        user_permissions: list[ResponsePermission] | None,
    ) -> list[FilmDB] | None:
        films = await self._get_search(
            page_number=page_number,
            page_size=page_size,
            search_query=search_query,
            field=field,
            model=FilmDB,
            user_permissions=user_permissions,
        )
        if not films:
            return None

        return await self.__get_allowed_films(films, user_permissions)

    async def __get_films_from_elastic(
        self,
        page_number: int,
        page_size: int,
        genre_uuid: str | None,
        sort_: str | None,
    ) -> list[FilmDB] | None:
        query = None
        sort = None
        if sort_:
            sort = []
            sort.append({sort_[1:]: "desc"}) if sort_[
                0
            ] == "-" else sort.append({sort_: "asc"})
        if genre_uuid:
            query = {
                "nested": {
                    "path": "genre",
                    "query": {
                        "bool": {
                            "must": [{"match": {"genre.uuid": genre_uuid}}]
                        }
                    },
                }
            }
        return await self._db.get_all(
            page_number=page_number,
            page_size=page_size,
            model=FilmDB,
            index=self._index,
            filter_path="hits.hits._source",
            query=query,
            sort=sort,
        )

    async def __get_allowed_films(
        self,
        films: list[FilmDB],
        user_permissions: list[ResponsePermission] | None,
    ):
        if user_permissions:
            user_permissions_set = {
                permission.name for permission in user_permissions
            }
        else:
            user_permissions_set = set()
        allowed_films = []
        for film in films:
            film_permissions_set = (
                {permission.get("name") for permission in film.permissions}
                if film.permissions
                else set()
            )
            if film_permissions_set.issubset(user_permissions_set):
                allowed_films.append(film)
        if not allowed_films:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Not enough permissions to view.",
            )
        return allowed_films


@lru_cache
def get_film_service(
    cache: RedisCache = Depends(get_redis),
    db: ElasticDB = Depends(get_elastic),
) -> FilmService:
    return FilmService(
        cache=cache,
        cache_ex=settings.cache_ex_for_films,
        db=db,
    )
