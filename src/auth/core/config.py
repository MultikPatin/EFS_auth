import os
from logging import config as logging_config

from async_fastapi_jwt_auth import AuthJWT

# from dotenv.main import find_dotenv, load_dotenv
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.auth.core.logger import LOGGING
from src.core.configs.postgres import PostgresSettings
from src.core.configs.redis import RedisSettings

# load_dotenv(find_dotenv(".env.auth"))

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./infra/var/auth/.env.api",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    postgres: PostgresSettings = PostgresSettings(
        _env_file="./infra/var/auth/.env.postgres",
        _env_file_encoding="utf-8",
    )
    #
    redis: RedisSettings = RedisSettings(
        _env_file="./infra/var/auth/.env.redis",
        _env_file_encoding="utf-8",
    )

    name: str = Field(..., alias="API_PROJECT_NAME")
    description: str = Field(..., alias="API_PROJECT_DESCRIPTION")
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

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


settings = Settings()


@AuthJWT.load_config
def get_config():
    return Settings()
