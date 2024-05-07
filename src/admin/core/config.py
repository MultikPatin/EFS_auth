from pydantic import Field, SecretStr
from pydantic_settings.main import SettingsConfigDict

from src.core.configs.base import ProjectSettings
from src.core.configs.postgres import (
    PostgresAuthSettings,
    PostgresContentSettings,
)


class Settings(ProjectSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    postgres_content: PostgresContentSettings = PostgresContentSettings()
    postgres_auth: PostgresAuthSettings = PostgresAuthSettings()
    host: str = Field(..., alias="ADMIN_API_HOST")
    port: int = Field(..., alias="ADMIN_API_PORT")
    allowed_hosts: str = Field(default=..., alias="ADMIN_ALLOWED_HOSTS")
    debug: str = Field(default=..., alias="ADMIN_DEBUG")
    secret_key: SecretStr = Field(default=..., alias="ADMIN_SECRET_KEY")

    @property
    def get_debug(self) -> bool:
        return self.debug == "True"

    @property
    def get_allowed_hosts(self) -> list:
        return self.allowed_hosts.split(",")


settings = Settings()

if settings.debug:
    print(settings.model_dump())
