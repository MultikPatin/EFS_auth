from logging import config as logging_config

from async_fastapi_jwt_auth import AuthJWT
from pydantic import Field, SecretStr

from src.configs.google import GoogleSettings
from src.configs.loader import LoaderSettings
from src.configs.logger import LOGGING
from src.configs.postgres import PostgresSettings
from src.configs.token import TokenSettings

from src.configs.utils import EnvSettings, FastApiSettings
from src.configs.redis import RedisSettings

logging_config.dictConfig(LOGGING)

PREFIX_BASE_ROUTE = "/api/v1"


class AppSettings(FastApiSettings):
    pass


class StartUpSettings(FastApiSettings):
    empty_role_name: str = Field(..., alias="EMPTY_ROLE_NAME")
    empty_role_description: str = Field(..., alias="EMPTY_ROLE_DESCRIPTION")
    admin_email: str = Field(..., alias="ADMIN_EMAIL")
    admin_password: SecretStr = Field(..., alias="ADMIN_PASSWORD")


class Settings(EnvSettings):
    app: AppSettings = AppSettings()
    start_up: StartUpSettings = StartUpSettings()
    token: TokenSettings = TokenSettings()
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()

    loader: LoaderSettings = LoaderSettings()

    google: GoogleSettings = GoogleSettings()
    google_config: dict = loader.get_JSON_config(loader.google_url)


settings = Settings()


@AuthJWT.load_config
def get_config():
    return Settings().token


if settings.app.debug:
    print(settings.model_dump())
