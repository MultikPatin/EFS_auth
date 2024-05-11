import json
from logging import Logger

import backoff
import elasticsearch.exceptions
from elasticsearch import Elasticsearch, helpers


class ElasticLoader:
    __logger: Logger = None

    def __init__(
        self,
        connection: Elasticsearch,
        index_name: str,
        index_data: dict,
        logger: Logger,
    ) -> None:
        self.__es = connection
        self.__index_name = index_name
        self.__logger = logger
        self.create_index(index_data)

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=elasticsearch.exceptions.ConnectionError,
    )
    def create_index(self, index_data: dict) -> None:
        """
        Создание ES индекса.
        """
        if not self.__es.ping():
            raise elasticsearch.exceptions.ConnectionError
        if not self.__es.indices.exists(index=self.__index_name):
            self.__es.indices.create(
                index=self.__index_name,
                settings=index_data["settings"],
                mappings=index_data["mappings"],
            )
            self.__logger.info(
                "Creating an index %s with the following schemes: %s and %s",
                self.__index_name,
                json.dumps(index_data["settings"], indent=2),
                json.dumps(index_data["mappings"], indent=2),
            )

    def load(self, data: list[dict]) -> None:
        """
        Загружаем данные пачками в ElasticSearch
        """
        actions = [
            {
                "_index": self.__index_name,
                "_id": row["uuid"],
                "_source": row,
            }
            for row in data
        ]
        helpers.bulk(self.__es, actions)
        self.__logger.info(
            "Loaded %s rows to index %s", len(data), self.__index_name
        )
