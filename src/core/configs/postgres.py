from pydantic import SecretStr
from pydantic.fields import Field
from sqlalchemy import URL

from src.core.configs.base import ServiceSettings


class PostgresSettings(ServiceSettings):
    """
    This class is used to store the Postgres connection settings.
    """

    database: str = Field(..., alias="POSTGRES_DB")
    user: str = Field(..., alias="POSTGRES_USER")
    password: SecretStr = Field(..., alias="POSTGRES_PASSWORD")
    host: str = Field(..., alias="POSTGRES_HOST")
    port: int = Field(..., alias="POSTGRES_PORT")
    host_local: str = Field(..., alias="POSTGRES_HOST_LOCAL")
    port_local: int = Field(..., alias="POSTGRES_PORT_LOCAL")
    sqlalchemy_echo: bool = Field("True", alias="SQLALCHEMY_ECHO")

    @property
    def postgres_connection_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.correct_host(),
            port=self.correct_port(),
            database=self.database,
        )


async def get_postgres_settings() -> PostgresSettings:
    return PostgresSettings()


class PostgresContentSettings(PostgresSettings):
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
    sqlalchemy_echo: bool = Field("True", alias="CONTENT_SQLALCHEMY_ECHO")


async def get_postgres_content_settings() -> PostgresContentSettings:
    return PostgresContentSettings()


class PostgresAuthSettings(PostgresContentSettings):
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
    sqlalchemy_echo: bool = Field("True", alias="AUTH_SQLALCHEMY_ECHO")


async def get_postgres_auth_settings() -> PostgresAuthSettings:
    return PostgresAuthSettings()
