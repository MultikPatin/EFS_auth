import logging
import time
from datetime import datetime

import backoff
import psycopg2

from src.core.utils.logger import create_logger
from src.etl_permission.config.base import settings
from src.etl_permission.helpers.extractor import PostgresExtractor
from src.etl_permission.helpers.loader import PostgresLoader
from src.etl_permission.helpers.state import JsonFileStorage, State


@backoff.on_exception(wait_gen=backoff.expo, exception=ConnectionError)
@backoff.on_exception(
    wait_gen=backoff.expo, exception=(psycopg2.Error, psycopg2.OperationalError)
)
def etl(
    logger: logging.Logger,
    extractor: PostgresExtractor,
    state: State,
    loader: PostgresLoader,
) -> None:
    last_sync_timestamp = state.get_state("last_sync_timestamp")
    logger.info("The last sync was %s", last_sync_timestamp)

    row_generator = extractor.extract(str(last_sync_timestamp))
    loader.save_table(row_generator, settings.permission_fields)
    state.set_state("last_sync_timestamp", str(datetime.utcnow()))


if __name__ == "__main__":
    logger = create_logger("ETL permissions Main")
    state = State(JsonFileStorage(file_path="state.json"))

    with (
        psycopg2.connect(
            **settings.postgres_content.psycopg2_connect
        ) as pg_content_conn,
        psycopg2.connect(
            **settings.postgres_auth.psycopg2_connect
        ) as pg_auth_conn,
    ):
        extractor = PostgresExtractor(
            connection=pg_auth_conn,
            buffer_size=settings.buffer_size,
            stmt=settings.extractor_stmt,
            logger=create_logger("ETL permissions PostgresExtractor"),
        )
        loader = PostgresLoader(
            connection=pg_content_conn,
            stmt=settings.load_stmt,
            logger=create_logger("ETL permissions PostgresLoader"),
        )

        while True:
            etl(logger, extractor, state, loader)
            logger.info("Pause for %s seconds", settings.sleep_time)
            time.sleep(settings.sleep_time)
