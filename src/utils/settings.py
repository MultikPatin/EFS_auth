import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.fields import Field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


class ServiceSettings(EnvSettings):
    host: str = ""
    port: int = 0
    host_local: str = "localhost"
    port_local: int = 8000
    local: bool = Field(default=True)

    def correct_host(self) -> str:
        return self.host_local if self.local else self.host

    def correct_port(self) -> int:
        return self.port_local if self.local else self.port


class FastApiSettings(ServiceSettings):
    name: str = Field(..., alias="API_NAME")
    description: str = Field(..., alias="API_DESCRIPTION")
    host: str = Field(..., alias="API_HOST")
    port: int = Field(..., alias="API_PORT")
    docs_url: str = Field(..., alias="API_DOCS_URL")
    openapi_url: str = Field(..., alias="API_OPENAPI_URL")
    base_dir: str = BASE_DIR
    debug: bool = Field(default=True)
