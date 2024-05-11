import logging
import os
import time
from datetime import datetime

import backoff
import psycopg2
from elasticsearch.exceptions import ConnectionError

from src.core.db.clients.elastic import elastic_search_connection
from src.core.utils.logger import create_logger
from src.etl_content.config.base import settings
from src.etl_content.helpers.extractor import PostgresExtractor
from src.etl_content.helpers.loader import ElasticLoader
from src.etl_content.helpers.state import JsonFileStorage, State
from src.etl_content.helpers.transformer import BaseTransformer

etl_name = os.getenv("ETL_NAME")


@backoff.on_exception(wait_gen=backoff.expo, exception=ConnectionError)
@backoff.on_exception(
    wait_gen=backoff.expo, exception=(psycopg2.Error, psycopg2.OperationalError)
)
def etl(
    logger: logging.Logger,
    extractor: PostgresExtractor,
    transformer: BaseTransformer,
    state: State,
    loader: ElasticLoader,
) -> None:
    """
    ETL процесс перекачки данных из PostgresSQL в Elasticsearch
    """
    last_sync_timestamp = state.get_state("last_sync_timestamp")
    logger.info("The last sync was %s", last_sync_timestamp)

    for extracted_part in extractor.extract(str(last_sync_timestamp)):
        data = transformer.transform(extracted_part)
        loader.load(data)
        state.set_state("last_sync_timestamp", str(datetime.utcnow()))


if __name__ == "__main__":
    logger = create_logger(f"ETL {etl_name.upper()} Main")
    state = State(JsonFileStorage(file_path="state.json"))

    with (
        elastic_search_connection(settings.elastic.get_host) as el_conn,
        psycopg2.connect(**settings.postgres.psycopg2_connect) as pg_conn,
    ):
        match etl_name:
            case "movies":
                from src.etl_content.config.movies import (
                    ELASTIC_DATA,
                    SQL_QUERY,
                )
                from src.etl_content.movies.transformer import Transformer

                transformer = Transformer()
                stmt = SQL_QUERY
                index_name = "movies"
                index_data = ELASTIC_DATA
            case "genres":
                from src.etl_content.config.genres import (
                    ELASTIC_DATA,
                    SQL_QUERY,
                )
                from src.etl_content.genres.transformer import Transformer

                transformer = Transformer()
                stmt = SQL_QUERY
                index_name = "genres"
                index_data = ELASTIC_DATA
            case "persons":
                from src.etl_content.config.persons import (
                    ELASTIC_DATA,
                    SQL_QUERY,
                )
                from src.etl_content.persons.transformer import Transformer

                transformer = Transformer()
                stmt = SQL_QUERY
                index_name = "persons"
                index_data = ELASTIC_DATA
            case _:
                raise ValueError(f"Unknown index name: {etl_name}")
        extractor = PostgresExtractor(
            connection=pg_conn,
            buffer_size=settings.buffer_size,
            stmt=stmt,
            logger=create_logger(f"ETL {etl_name.upper()} PostgresExtractor"),
        )
        loader = ElasticLoader(
            connection=el_conn,
            index_name=index_name,
            index_data=index_data,
            logger=create_logger(f"ETL {etl_name.upper()} ElasticLoader"),
        )

        while True:
            etl(logger, extractor, transformer, state, loader)
            logger.info("Pause for %s seconds", settings.sleep_time)
            time.sleep(settings.sleep_time)
