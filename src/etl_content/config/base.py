# from dotenv.main import find_dotenv, load_dotenv
from pydantic.fields import Field
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict

from src.core.configs.elastic import ElasticSettings
from src.core.configs.postgres import PostgresSettings

# load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./infra/var/content/.env.etl",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    postgres: PostgresSettings = PostgresSettings(
        _env_file="./infra/var/content/.env.postgres",
        _env_file_encoding="utf-8",
    )
    elastic: ElasticSettings = ElasticSettings(
        _env_file="./infra/var/content/.env.elastic",
        _env_file_encoding="utf-8",
    )
    buffer_size: int = Field(..., alias="ETL_BUFFERED_ROWS")
    sleep_time: int = Field(..., alias="ETL_SLEEP_TIME")


settings = Settings()

_ELASTIC_SETTINGS = {
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
