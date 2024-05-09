from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from logging import Logger

from psycopg2.extensions import connection as _connection


@dataclass(frozen=True)
class Permission:
    id: str
    name: str
    description: str
    created: datetime
    modified: datetime


class PostgresExtractor:
    __cursor = None
    __logger: Logger = None

    def __init__(
        self,
        connection: _connection,
        stmt: str,
        buffer_size: int,
        logger: Logger,
    ) -> None:
        self.__connection = connection
        self.__buffer_size = buffer_size
        self.__stmt = stmt
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
                transformed_part = []
                for row in rows:
                    permission = Permission(
                        id=row["uuid"],
                        name=row["name"],
                        description=row["description"],
                        created=row["created_at"],
                        modified=row["updated_at"],
                    )
                    transformed_part.append(permission)
                self.__logger.info(
                    "Extracted %s rows for permission", len(rows)
                )
                yield transformed_part
            else:
                self.__logger.info("No changes found for permission")
                self.__cursor.close()
                break
