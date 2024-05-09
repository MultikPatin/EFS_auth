import io
from collections.abc import Iterator
from logging import Logger

from psycopg2.extensions import connection as _connection


class PostgresLoader:
    __cursor = None
    __logger: Logger = None

    def __init__(self, connection: _connection, stmt: str, logger: Logger):
        self.__connection = connection
        self.__logger = logger
        self.__stmt = stmt

    def save_table(self, rows: Iterator, fields: list):
        self.__cursor = self.__connection.cursor()
        self.__save_table(rows, fields)
        self.__logger.debug(
            "Завершено копирование данных для таблицы permission"
        )
        self.__cursor.close()

    def __save_table(self, rows: Iterator, fields: list):
        for row in rows:
            columns = (getattr(row, field) for field in fields)
            string_io = self.__get_row_in_string_io(columns)
            try:
                self.__cursor.copy_expert(self.__stmt, string_io, 1024)
            except Exception as error:
                self.__connection.rollback()
                string_io.seek(0)
                self.logger.error(
                    f"==> При копирование данных {string_io.readline()} "
                    f"возникла ошибка: {error}"
                )

    def __get_row_in_string_io(self, columns) -> io.StringIO:
        string_io = io.StringIO()
        string_io.write("|".join(map(self.__clean_csv_value, columns)))
        string_io.seek(0)
        return string_io

    @staticmethod
    def __clean_csv_value(value) -> str:
        if value is None:
            return r"null"
        return str(value).replace("\n", "\\n")
