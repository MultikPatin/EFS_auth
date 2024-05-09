from collections.abc import Iterator
from logging import Logger

from psycopg2.extensions import connection as _connection


class PostgresExtractor:
    __cursor = None
    __logger: Logger = None

    def __init__(
        self,
        connection: _connection,
        buffer_size: int,
        logger: Logger,
    ) -> None:
        self.__connection = connection
        self.__buffer_size = buffer_size
        self.__logger = logger

    def extract(self, extract_timestamp: str) -> Iterator:
        """
        Метод чтения данных пачками.
        Ищем строки, удовлетворяющие условию - при нахождении записываем
        в хранилище состояния id
        """
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute(self.__stmt.format(extract_timestamp))

        while True:
            rows = self.__cursor.fetchmany(self.__buffer_size)
            if rows:
                self.__logger.info(
                    "Extracted %s rows for permission", len(rows)
                )
                yield rows
            else:
                self.__logger.info("No changes found for permission")
                self.__cursor.close()
                break
