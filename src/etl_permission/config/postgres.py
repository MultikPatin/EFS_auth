from psycopg2.extras import DictCursor

from src.core.configs.postgres import (
    PostgresAuthSettings,
    PostgresContentSettings,
)


class PostgresContentSettingsPsyco(PostgresContentSettings):
    @property
    def psycopg2_connect(self) -> dict:
        return {
            "dbname": self.database,
            "user": self.user,
            "password": self.password.get_secret_value(),
            "host": self.correct_host(),
            "port": self.correct_port(),
            "cursor_factory": DictCursor,
        }


class PostgresAuthSettingsPsyco(PostgresAuthSettings):
    @property
    def psycopg2_connect(self) -> dict:
        return {
            "dbname": self.database,
            "user": self.user,
            "password": self.password.get_secret_value(),
            "host": self.correct_host(),
            "port": self.correct_port(),
            "cursor_factory": DictCursor,
        }
