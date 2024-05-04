from logging import config as logging_config

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from src.content.core.logger import LOGGING
from src.core.configs.base import ProjectSettings
from src.core.configs.elastic import ElasticSettings
from src.core.configs.redis import RedisSettings

logging_config.dictConfig(LOGGING)


class Settings(ProjectSettings):
    model_config = SettingsConfigDict(
        env_file="./infra/var/content/.env.api",
        env_file_encoding="utf-8",
    )
    elastic: ElasticSettings = ElasticSettings(
        _env_file="./infra/var/content/.env.elastic",
        _env_file_encoding="utf-8",
    )
    redis: RedisSettings = RedisSettings(
        _env_file="./infra/var/content/.env.redis",
        _env_file_encoding="utf-8",
    )

    docs_url: str = Field(..., alias="API_DOCS_URL")
    openapi_url: str = Field(..., alias="API_OPENAPI_URL")
    host: str = Field(..., alias="API_HOST")
    port: int = Field(..., alias="API_PORT")

    cache_ex_for_films: int = Field(
        ..., alias="API_CACHE_EXPIRE_FOR_FILM_SERVICE"
    )
    cache_ex_for_genres: int = Field(
        ..., alias="API_CACHE_EXPIRE_FOR_GENRES_SERVICE"
    )
    cache_ex_for_persons: int = Field(
        ..., alias="API_CACHE_EXPIRE_FOR_PERSON_SERVICE"
    )


settings = Settings()

if settings.debug:
    print(settings.model_dump())
