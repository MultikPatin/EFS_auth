from logging import config as logging_config

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import SettingsConfigDict

from src.content.core.logger import LOGGING
from src.core.configs.base import ProjectSettings
from src.core.configs.elastic import ElasticContentSettings
from src.core.configs.redis import RedisContentSettings

logging_config.dictConfig(LOGGING)
load_dotenv()


class Settings(ProjectSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    elastic: ElasticContentSettings = ElasticContentSettings()
    redis: RedisContentSettings = RedisContentSettings()
    name: str = Field(..., alias="CONTENT_PROJECT_NAME")
    description: str = Field(..., alias="CONTENT_PROJECT_DESCRIPTION")
    host: str = Field(..., alias="CONTENT_API_HOST")
    port: int = Field(..., alias="CONTENT_API_PORT")
    docs_url: str = Field(..., alias="CONTENT_API_DOCS_URL")
    openapi_url: str = Field(..., alias="CONTENT_API_OPENAPI_URL")

    cache_ex_for_films: int = Field(
        ..., alias="CONTENT_API_CACHE_EXPIRE_FOR_FILM_SERVICE"
    )
    cache_ex_for_genres: int = Field(
        ..., alias="CONTENT_API_CACHE_EXPIRE_FOR_GENRES_SERVICE"
    )
    cache_ex_for_persons: int = Field(
        ..., alias="CONTENT_API_CACHE_EXPIRE_FOR_PERSON_SERVICE"
    )


settings = Settings()

if settings.debug:
    print(settings.model_dump())
