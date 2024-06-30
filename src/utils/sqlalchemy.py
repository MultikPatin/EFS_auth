from pydantic import SecretStr
from pydantic.fields import Field
from sqlalchemy import URL

from src.utils.settings import ServiceSettings


class SQLAlchemyConnection(ServiceSettings):
    database: str
    user: str
    password: SecretStr
    sqlalchemy_echo: bool = Field(default=True)

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
