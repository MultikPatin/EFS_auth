import os
from logging import config as logging_config

# from dotenv.main import find_dotenv, load_dotenv
from pydantic.fields import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.content.core.logger import LOGGING
from src.core.configs.elastic import ElasticSettings
from src.core.configs.redis import RedisSettings

# load_dotenv(find_dotenv("env/.env.content"))

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./infra/var/content/.env.api",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    elastic: ElasticSettings = ElasticSettings(
        _env_file="./infra/var/content/.env.elastic",
        _env_file_encoding="utf-8",
    )
    redis: RedisSettings = RedisSettings(
        _env_file="./infra/var/content/.env.redis",
        _env_file_encoding="utf-8",
    )
    name: str = Field(..., alias="API_PROJECT_NAME")
    description: str = Field(..., alias="API_PROJECT_DESCRIPTION")
    docs_url: str = Field(..., alias="API_DOCS_URL")
    openapi_url: str = Field(..., alias="API_OPENAPI_URL")
    host: str = Field(..., alias="API_HOST")
    port: int = Field(..., alias="API_PORT")

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
