from pathlib import Path

from split_settings.tools import include

from pydantic import Field, SecretStr
from pydantic_settings.main import SettingsConfigDict
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from .postgres import (
    ServiceSettings,
    PostgresAuthSettings,
    PostgresContentSettings,
)

load_dotenv()


class AdvancedSettings(ServiceSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    local: bool = Field("True", alias="LOCAL")
    postgres_content: PostgresContentSettings = PostgresContentSettings()
    postgres_auth: PostgresAuthSettings = PostgresAuthSettings()
    host: str = Field(..., alias="ADMIN_API_HOST")
    port: int = Field(..., alias="ADMIN_API_PORT")
    host_local: str = Field(..., alias="ADMIN_API_PORT_LOCAL")
    port_local: int = Field(..., alias="ADMIN_API_PORT_LOCAL")
    allowed_hosts: str = Field(default=..., alias="ADMIN_ALLOWED_HOSTS")
    debug: str = Field(default=..., alias="ADMIN_DEBUG")
    secret_key: SecretStr = Field(default=..., alias="ADMIN_SECRET_KEY")
    auth_host: str = Field(..., alias="AUTH_API_HOST")
    auth_port: int = Field(..., alias="AUTH_API_PORT")
    auth_host_local: str = Field(..., alias="AUTH_API_HOST_LOCAL")
    auth_port_local: int = Field(..., alias="AUTH_API_PORT_LOCAL")
    # superuser_name: str = Field(default=..., alias="ADMIN_SUPERUSER_USERNAME")
    superuser_password: SecretStr = Field(
        default=..., alias="ADMIN_SUPERUSER_PASSWORD"
    )
    superuser_mail: str = Field(default=..., alias="ADMIN_SUPERUSER_EMAIL")

    @property
    def get_debug(self) -> bool:
        return self.debug == "True"

    @property
    def get_allowed_hosts(self) -> list:
        return self.allowed_hosts.split(",")

    @property
    def get_api_login_url(self) -> str:
        rout = "/auth/v1/tokens/login/"
        if self.local:
            return f"http://{self.auth_host_local}:{self.auth_port_local}{rout}"
        return f"http://{self.auth_host}:{self.auth_port}{rout}"


ADVANCED_SETTINGS = AdvancedSettings()

if ADVANCED_SETTINGS.debug:
    print(ADVANCED_SETTINGS.model_dump())

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = ADVANCED_SETTINGS.secret_key.get_secret_value()
DEBUG = ADVANCED_SETTINGS.get_debug
ALLOWED_HOSTS = ADVANCED_SETTINGS.get_allowed_hosts

include(
    "components/apps.py",
    "components/middleware.py",
    "components/templates.py",
    "components/database.py",
    "components/auth.py",
)

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "ru-RU"

LOCALE_PATHS = ["movies/locale"]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "collected_static"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

AUTH_API_LOGIN_URL = ADVANCED_SETTINGS.get_api_login_url

AUTHENTICATION_BACKENDS = [
    "users.auth.CustomBackend",
]
