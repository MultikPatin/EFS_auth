from pydantic.fields import Field
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict

from src.core.configs.elastic import ElasticContentSettings
from src.core.configs.postgres import PostgresContentSettings
from src.core.utils.psycopg import PsycopgConnectMixin


class PostgresContentConnect(PostgresContentSettings, PsycopgConnectMixin):
    pass


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    postgres: PostgresContentConnect = PostgresContentConnect()
    elastic: ElasticContentSettings = ElasticContentSettings()
    buffer_size: int = Field(..., alias="ETL_CONTENT_BUFFERED_ROWS")
    sleep_time: int = Field(..., alias="ETL_CONTENT_SLEEP_TIME")


settings = Settings()

ELASTIC_SETTINGS = {
    "refresh_interval": "1s",
    "analysis": {
        "filter": {
            "english_stop": {"type": "stop", "stopwords": "_english_"},
            "english_stemmer": {
                "type": "stemmer",
                "language": "english",
            },
            "english_possessive_stemmer": {
                "type": "stemmer",
                "language": "possessive_english",
            },
            "russian_stop": {"type": "stop", "stopwords": "_russian_"},
            "russian_stemmer": {
                "type": "stemmer",
                "language": "russian",
            },
        },
        "analyzer": {
            "ru_en": {
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "english_stop",
                    "english_stemmer",
                    "english_possessive_stemmer",
                    "russian_stop",
                    "russian_stemmer",
                ],
            }
        },
    },
}
