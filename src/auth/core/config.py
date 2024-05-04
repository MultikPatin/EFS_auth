from logging import config as logging_config

from async_fastapi_jwt_auth import AuthJWT
from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict

from src.auth.core.logger import LOGGING
from src.core.configs.base import ProjectSettings
from src.core.configs.postgres import PostgresSettings
from src.core.configs.redis import RedisSettings

logging_config.dictConfig(LOGGING)


class Settings(ProjectSettings):
    model_config = SettingsConfigDict(
        env_file="./infra/env/auth/.env.api",
        env_file_encoding="utf-8",
    )
    postgres: PostgresSettings = PostgresSettings(
        _env_file="./infra/env/auth/.env.postgres",
        _env_file_encoding="utf-8",
    )
    redis: RedisSettings = RedisSettings(
        _env_file="./infra/env/auth/.env.redis",
        _env_file_encoding="utf-8",
    )

    docs_url: str = Field(..., alias="API_DOCS_URL")
    openapi_url: str = Field(..., alias="API_OPENAPI_URL")
    host: str = Field(..., alias="API_HOST")
    port: int = Field(..., alias="API_PORT")

    empty_role_name: str = Field(..., alias="EMPTY_ROLE_NAME")
    empty_role_description: str = Field(..., alias="EMPTY_ROLE_DESCRIPTION")

    admin_email: str = Field(..., alias="ADMIN_EMAIL")
    admin_password: SecretStr = Field(..., alias="ADMIN_PASSWORD")

    token_expire_time: int = Field(..., alias="TOKEN_EXPIRE_TIME")
    user_max_sessions: int = Field(..., alias="USER_MAX_SESSIONS")

    authjwt_secret_key: str = Field(..., alias="AUTHJWT_SECRET_KEY")
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = (
        Field(..., alias="AUTHJWT_COOKIE_CSRF_PROTECT") == "True"
    )
    authjwt_cookie_secure: bool = (
        Field(..., alias="AUTHJWT_COOKIE_SECURE") == "True"
    )


settings = Settings()


@AuthJWT.load_config
def get_config():
    return Settings()


if settings.debug:
    print(settings.model_dump())
