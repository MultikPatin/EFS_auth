from psycopg2.extras import DictCursor
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

    local: bool = Field("True", alias="LOCAL")
    host_local: str = Field("localhost", alias="POSTGRES_HOST_LOCAL")
    port_local: int = Field(5432, alias="POSTGRES_PORT_LOCAL")

    @property
    def postgres_connection_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self._correct_host(),
            port=self._correct_port(),
            database=self.database,
        )


class PostgresSettingsWithPsycoConnect(PostgresSettings):
    @property
    def psycopg2_connect(self) -> dict:
        return {
            "dbname": self.database,
            "user": self.user,
            "password": self.password.get_secret_value(),
            "host": self._correct_host(),
            "port": self._correct_port(),
            "cursor_factory": DictCursor,
        }
