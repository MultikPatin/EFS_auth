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
    host_local: str = Field(..., alias="CONTENT_API_HOST_LOCAL")
    port: int = Field(..., alias="CONTENT_API_PORT")
    port_local: int = Field(..., alias="CONTENT_API_PORT_LOCAL")
    auth_host: str = Field(..., alias="AUTH_API_HOST")
    auth_port: int = Field(..., alias="AUTH_API_PORT")
    auth_host_local: str = Field(..., alias="AUTH_API_HOST_LOCAL")
    auth_port_local: int = Field(..., alias="AUTH_API_PORT_LOCAL")
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
    authjwt_secret_key: str = Field(..., alias="AUTH_AUTHJWT_SECRET_KEY")
    authjwt_algorithm: str = Field(..., alias="AUTH_AUTHJWT_ALGORITHM")

    def get_api_roles_url(self) -> str:
        rout = "/auth/v1/roles/"
        if self.local:
            return f"http://{self.auth_host_local}:{self.auth_port_local}{rout}"
        return f"http://{self.auth_host}:{self.auth_port}{rout}"


settings = Settings()

if settings.debug:
    print(settings.model_dump())
