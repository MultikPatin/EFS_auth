import os

# from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic.fields import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

# load_dotenv(".env")
local = os.getenv("LOCAL", "True")


class PostgresSettings(BaseSettings):
    """
    This class is used to store the Postgres connection settings.
    """

    model_config = SettingsConfigDict(extra="ignore")
    database: str = Field(..., alias="POSTGRES_DB")
    user: str = Field(..., alias="POSTGRES_USER")
    password: SecretStr = Field(..., alias="POSTGRES_PASSWORD")
    host: str = Field(..., alias="POSTGRES_HOST")
    port: int = Field(..., alias="POSTGRES_PORT")

    def __correct_host(self) -> str:
        if local == "True":
            return "localhost"
        return self.host

    @property
    def postgres_connection_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.__correct_host(),
            port=self.port,
            database=self.database,
        )


# def get_postgres_settings() -> PostgresSettings:
#     return PostgresSettings()
