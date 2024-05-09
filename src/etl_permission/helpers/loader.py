from collections.abc import Generator
from logging import Logger

from psycopg2.extensions import connection as _connection


class PostgresLoader:
    __table_name = None
    __cursor = None
    __logger: Logger = None

    def __init__(self, connection: _connection, logger: Logger):
        self.__connection = connection
        self.__logger = logger

    def save_table(self, table_name: str, rows: Generator):
        self.__cursor = self.__connection.cursor()
        self.__table_name = table_name
        # self.__truncate_tables()
        # self.__drop_indexes()
        # self.__save_table(rows)
        self.__logger.debug(
            f"Завершено копирование данных для таблицы {self.__table_name}"
        )
        # self.__create_indexes()
        self.__cursor.close()

    # def __truncate_tables(self):
    #     stmt = f"TRUNCATE content.{self.__table_name} CASCADE"
    #     self.__cursor.execute(stmt)
    #     self.logger.debug(stmt)
    #
    # def __drop_indexes(self):
    #     stmt = "DROP INDEX IF EXISTS {field}"
    #     self.__indexes(stmt)
    #
    # def __create_indexes(self):
    #     stmt = "CREATE INDEX IF NOT EXISTS {field} ON content.{table} ({field})"
    #     self.__indexes(stmt)
    #
    # def __indexes(self, stmt: str):
    #     indexes = PG_INDEXES.get(self.__table_name)
    #     if indexes:
    #         for index in indexes:
    #             try:
    #                 self.__cursor.execute(
    #                     stmt.format(table=self.__table_name, field=index)
    #                 )
    #                 self.__connection.commit()
    #                 self.logger.debug(
    #                     stmt.format(table=self.__table_name, field=index)
    #                 )
    #             except Exception as error:
    #                 self.__connection.rollback()
    #                 self.logger.error("==> возникла ошибка: %s", error)
    #
    # def __save_table(self, rows: Generator):
    #     for row in rows:
    #         columns = (
    #             getattr(row, sqlite_field)
    #             for sqlite_field, postgres_field in TABLES[self.__table_name]
    #             if postgres_field is not None
    #         )
    #         string_io = self.__get_row_in_string_io(columns)
    #         stmt = f"""COPY content.{self.__table_name} FROM STDIN
    #                     (FORMAT 'csv', HEADER false, DELIMITER '|',
    #                     QUOTE E'\b', NULL 'null')"""
    #         try:
    #             self.__cursor.copy_expert(stmt, string_io, 1024)
    #         except Exception as error:
    #             self.__connection.rollback()
    #             string_io.seek(0)
    #             self.logger.error(
    #                 f"==> При копирование данных {string_io.readline()} "
    #                 f"возникла ошибка: {error}"
    #             )
    #
    # def __get_row_in_string_io(self, columns) -> io.StringIO:
    #     string_io = io.StringIO()
    #     string_io.write("|".join(map(self.__clean_csv_value, columns)))
    #     string_io.seek(0)
    #     return string_io
    #
    # @staticmethod
    # def __clean_csv_value(value) -> str:
    #     if value is None:
    #         return r"null"
    #     return str(value).replace("\n", "\\n")
