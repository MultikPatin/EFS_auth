from psycopg2.extras import DictCursor

from src.core.configs.postgres import PostgresSettings


class PostgresSettingsWithPsycoConnect(PostgresSettings):
    @property
    def psycopg2_connect(self) -> dict:
        return {
            "dbname": self.database,
            "user": self.user,
            "password": self.password.get_secret_value(),
            "host": self._correct_host(),
            "port": self._correct_port(),
            "cursor_factory": DictCursor,
        }
