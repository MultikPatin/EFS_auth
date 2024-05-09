from dotenv import load_dotenv
from pydantic.fields import Field
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict

from src.etl_permission.config.postgres import (
    PostgresAuthSettingsPsyco,
    PostgresContentSettingsPsyco,
)

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    postgres_content: PostgresContentSettingsPsyco = (
        PostgresContentSettingsPsyco()
    )
    postgres_auth: PostgresAuthSettingsPsyco = PostgresAuthSettingsPsyco()
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
    load_stmt: str = """
        COPY access.permission FROM STDIN
        (FORMAT 'csv', HEADER false, DELIMITER '|',
        QUOTE E'\b', NULL 'null')
        """
    permission_fields: list = [
        "id",
        "name",
        "description",
        "created",
        "modified",
    ]


settings = Settings()
