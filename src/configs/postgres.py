from pydantic import SecretStr
from pydantic.fields import Field

from src.utils.sqlalchemy import SQLAlchemyConnection


class PostgresSettings(SQLAlchemyConnection):
    """
    This class is used to store the Postgres content db connection settings.
    """

    db_name: str = Field(..., alias="POSTGRES_DB")
    user: str = Field(..., alias="POSTGRES_USER")
    password: SecretStr = Field(..., alias="POSTGRES_PASSWORD")
    host: str = Field(..., alias="POSTGRES_HOST")
    port: int = Field(..., alias="POSTGRES_PORT")
    host_local: str = Field(default="localhost", alias="POSTGRES_HOST_LOCAL")
    port_local: int = Field(default=5432, alias="POSTGRES_PORT_LOCAL")
