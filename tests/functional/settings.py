from typing import Any

from pydantic.fields import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# from dotenv.main import find_dotenv, load_dotenv

# load_dotenv(find_dotenv(".env"))


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            "./infra/var/auth/.env.api",
            "./infra/var/auth/.env.postgres",
            "./infra/var/auth/.env.redis",
            ".env",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )
    local: str = Field("True", alias="LOCAL")

    postgres_database: str = Field(default=..., alias="POSTGRES_DB")
    postgres_user: str = Field(default=..., alias="POSTGRES_USER")
    postgres_password: str = Field(default=..., alias="POSTGRES_PASSWORD")
    postgres_host: str = Field(default=..., alias="AUTH_POSTGRES_HOST")
    postgres_port: int = Field(default=..., alias="POSTGRES_PORT")
    postgres_port_local: int = Field(default=..., alias="AUTH_POSTGRES_PORT")

    redis_host: str = Field(default=..., alias="AUTH_REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_port_local: int = Field(default=6379, alias="AUTH_REDIS_PORT")

    name: str = Field(..., alias="API_PROJECT_NAME")
    description: str = Field(..., alias="API_PROJECT_DESCRIPTION")
    docs_url: str = Field(..., alias="API_DOCS_URL")
    openapi_url: str = Field(..., alias="API_OPENAPI_URL")
    api_host: str = Field(..., alias="API_HOST")
    api_port: int = Field(..., alias="API_PORT")

    token_expire_time: int = Field(..., alias="TOKEN_EXPIRE_TIME")
    user_max_sessions: int = Field(..., alias="USER_MAX_SESSIONS")

    secret_key: str = Field(..., alias="AUTHJWT_SECRET_KEY")

    @property
    def psycopg2_connect(self) -> dict:
        if self.local == "True":
            host = self.postgres_host
            port = self.postgres_port_local
        else:
            host = self.postgres_host
            port = self.postgres_port

        return {
            "dbname": self.postgres_database,
            "user": self.postgres_user,
            "password": self.postgres_password,
            "host": host,
            "port": port,
        }

    @property
    def get_redis_host(self) -> dict[str, Any]:
        if self.local == "True":
            return {"host": self.redis_host, "port": self.redis_port_local}
        return {"host": self.redis_host, "port": self.redis_port}

    @property
    def get_api_host(self) -> str:
        if self.local == "True":
            return f"127.0.0.1:{self.api_port}"
        return f"{self.api_host}:{self.api_port}"


settings = TestSettings()
