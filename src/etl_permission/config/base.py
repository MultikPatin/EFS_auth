from dataclasses import dataclass
from datetime import datetime

from dotenv import load_dotenv
from pydantic.fields import Field
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict

from src.core.configs.postgres import (
    PostgresAuthSettings,
    PostgresContentSettings,
)
from src.core.utils.psycopg import PsycopgConnectMixin

load_dotenv()


class PostgresContentConnect(PostgresContentSettings, PsycopgConnectMixin):
    pass


class PostgresAuthConnect(PostgresAuthSettings, PsycopgConnectMixin):
    pass


@dataclass(frozen=True)
class Permission:
    id: str
    name: str
    description: str
    created: datetime
    modified: datetime


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    postgres_content: PostgresContentConnect = PostgresContentConnect()
    postgres_auth: PostgresAuthConnect = PostgresAuthConnect()
    buffer_size: int = Field(..., alias="ETL_PERMISSION_BUFFERED_ROWS")
    sleep_time: int = Field(..., alias="ETL_PERMISSION_SLEEP_TIME")
    extractor_stmt: str = """
        SELECT
            p.uuid,
            p.name,
            p.description,
            p.created_at,
            p.updated_at
        FROM public.permissions as p
        WHERE p.updated_at > '{}'
        GROUP BY p.uuid
        ORDER BY p.updated_at DESC
        """


settings = Settings()
