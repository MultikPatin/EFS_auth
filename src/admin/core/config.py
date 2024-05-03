from pydantic import SecretStr
from pydantic.fields import Field
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict

from src.core.configs.postgres import PostgresSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    postgres: PostgresSettings = PostgresSettings(
        _env_file="./infra/var/content/.env.postgres",
        _env_file_encoding="utf-8",
    )
    allowed_hosts: str = Field(default=..., alias="ALLOWED_HOSTS")
    debug: str = Field(default=..., alias="DEBUG")
    secret_key: SecretStr = Field(default=..., alias="SECRET_KEY")
    superuser_name: str = Field(default=..., alias="DJANGO_SUPERUSER_USERNAME")
    superuser_password: SecretStr = Field(
        default=..., alias="DJANGO_SUPERUSER_PASSWORD"
    )
    superuser_mail: str = Field(default=..., alias="DJANGO_SUPERUSER_EMAIL")

    @property
    def get_debug(self) -> bool:
        return self.debug == "True"

    @property
    def get_allowed_hosts(self) -> list:
        return self.allowed_hosts.split(",")


settings = Settings()
