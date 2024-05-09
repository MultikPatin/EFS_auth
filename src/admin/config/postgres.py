from pydantic import SecretStr
from pydantic.fields import Field
from pydantic_settings import BaseSettings


class ServiceSettings(BaseSettings):
    host: str = ""
    port: int = 0
    host_local: str = ""
    port_local: int = 0
    local: bool = Field("True", alias="LOCAL")

    def correct_host(self) -> str:
        if self.local:
            return self.host_local
        return self.host

    def correct_port(self) -> int:
        if self.local:
            return self.port_local
        return self.port


class PostgresContentSettings(ServiceSettings):
    """
    This class is used to store the Postgres content db connection settings.
    """

    database: str = Field(..., alias="CONTENT_POSTGRES_DB")
    user: str = Field(..., alias="CONTENT_POSTGRES_USER")
    password: SecretStr = Field(..., alias="CONTENT_POSTGRES_PASSWORD")
    host: str = Field(..., alias="CONTENT_POSTGRES_HOST")
    port: int = Field(..., alias="CONTENT_POSTGRES_PORT")
    host_local: str = Field(..., alias="CONTENT_POSTGRES_HOST_LOCAL")
    port_local: int = Field(..., alias="CONTENT_POSTGRES_PORT_LOCAL")


class PostgresAuthSettings(ServiceSettings):
    """
    This class is used to store the Postgres auth db connection settings.
    """

    database: str = Field(..., alias="AUTH_POSTGRES_DB")
    user: str = Field(..., alias="AUTH_POSTGRES_USER")
    password: SecretStr = Field(..., alias="AUTH_POSTGRES_PASSWORD")
    host: str = Field(..., alias="AUTH_POSTGRES_HOST")
    port: int = Field(..., alias="AUTH_POSTGRES_PORT")
    host_local: str = Field(..., alias="AUTH_POSTGRES_HOST_LOCAL")
    port_local: int = Field(..., alias="AUTH_POSTGRES_PORT_LOCAL")
