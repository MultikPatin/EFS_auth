from pydantic.fields import Field
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict

from src.etl_permission.config.postgres import (
    PostgresAuthSettingsPsyco,
    PostgresContentSettingsPsyco,
)


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


settings = Settings()
