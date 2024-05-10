from collections.abc import Iterator
from dataclasses import fields
from logging import Logger

from psycopg2.extensions import connection as _connection

from src.etl_permission.config.base import Permission


class PostgresLoader:
    __cursor = None
    __logger: Logger = None

    def __init__(self, connection: _connection, logger: Logger):
        self.__connection = connection
        self.__logger = logger

    def save_table(self, rows: Iterator):
        self.__cursor = self.__connection.cursor()
        self.__save_table(rows)
        self.__logger.debug(
            "Завершено копирование данных для таблицы permission"
        )
        self.__cursor.close()

    def __save_table(self, rows: Iterator):
        column = self.__get_column_names_str()
        for row in rows:
            values = self.__get_insert_values(row)
            self.__upsert_data(column, values)

    def __upsert_data(self, column: str, values: str):
        print(values)
        stmt = (
            f"INSERT INTO access.permission ({column}) VALUES {values} "
            f"ON CONFLICT (id) DO UPDATE SET "
            f"name=EXCLUDED.name, "
            f"description=EXCLUDED.description, "
            f"created=EXCLUDED.created, "
            f"modified=EXCLUDED.modified;"
        )
        print(stmt)
        self.__cursor.execute(stmt)
        self.__connection.commit()

    @staticmethod
    def __get_column_names_str() -> str:
        column_names = [field.name for field in fields(Permission)]
        column_names_str = ", ".join(column_names)
        return column_names_str

    @staticmethod
    def __get_insert_values(rows: list[Permission]) -> str:
        values = [
            (
                row.id,
                row.name,
                row.description,
                str(row.created),
                str(row.modified),
            )
            for row in rows
        ]
        values = ", ".join(str(value) for value in values)
        return values
