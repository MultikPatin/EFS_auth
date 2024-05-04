import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    host: str
    port: int
    host_local: str = ""
    port_local: int = 0
    local: bool = Field("True", alias="LOCAL")

    def _correct_host(self) -> str:
        if self.local:
            return self.host_local
        return self.host

    def _correct_port(self) -> int:
        if self.local:
            return self.port_local
        return self.port


class ProjectSettings(ServiceSettings):
    name: str = Field(..., alias="PROJECT_NAME")
    description: str = Field(..., alias="PROJECT_DESCRIPTION")
    debug: bool = Field("True", alias="DEBUG")
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
