from pydantic import Field, SecretStr
from pydantic_settings.main import SettingsConfigDict

from src.core.configs.base import ProjectSettings
from src.core.configs.postgres import PostgresSettings


class Settings(ProjectSettings):
    model_config = SettingsConfigDict(
        env_file="./infra/env/admin/.env.api",
        env_file_encoding="utf-8",
    )
    postgres_content: PostgresSettings = PostgresSettings(
        _env_file="./infra/env/content/.env.postgres",
        _env_file_encoding="utf-8",
    )
    postgres_auth: PostgresSettings = PostgresSettings(
        _env_file="./infra/env/auth/.env.postgres",
        _env_file_encoding="utf-8",
    )
    allowed_hosts: str = Field(default=..., alias="ALLOWED_HOSTS")
    debug: str = Field(default=..., alias="DEBUG")
    secret_key: SecretStr = Field(default=..., alias="SECRET_KEY")

    @property
    def get_debug(self) -> bool:
        return self.debug == "True"

    @property
    def get_allowed_hosts(self) -> list:
        return self.allowed_hosts.split(",")


settings = Settings()

if settings.debug:
    print(settings.model_dump())
