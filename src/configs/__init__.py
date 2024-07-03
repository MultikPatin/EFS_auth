from logging import config as logging_config

from async_fastapi_jwt_auth import AuthJWT

from src.configs.jeager import JaegerSettings
from src.configs.logger import LOGGING
from src.configs.notifications_api import NotificationApiSettings
from src.configs.oauth2_google import Oauth2GoogleSettings
from src.configs.postgres import PostgresSettings
from src.configs.redis import RedisSettings
from src.configs.sentry import SentrySettings
from src.configs.start_up import StartUpSettings
from src.configs.token import TokenSettings

from src.utils.settings import EnvSettings, FastApiSettings

__all__ = [
    "settings",
    "LOGGING",
    "PostgresSettings",
    "StartUpSettings",
    "Oauth2GoogleSettings",
    "TokenSettings",
]

logging_config.dictConfig(LOGGING)


class AppSettings(FastApiSettings):
    pass


class Oauth2Settings(FastApiSettings):
    google: Oauth2GoogleSettings = Oauth2GoogleSettings()


class ThirdPartyApiSettings(FastApiSettings):
    notification: NotificationApiSettings = NotificationApiSettings()


class Settings(EnvSettings):
    app: AppSettings = AppSettings()
    start_up: StartUpSettings = StartUpSettings()
    token: TokenSettings = TokenSettings()
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()
    oauth2: Oauth2Settings = Oauth2Settings()
    jaeger: JaegerSettings = JaegerSettings()
    third_party_api: ThirdPartyApiSettings = ThirdPartyApiSettings()
    sentry: SentrySettings = SentrySettings()


settings = Settings()


@AuthJWT.load_config
def get_config():
    return Settings().token


if settings.app.debug:
    print(settings.model_dump())