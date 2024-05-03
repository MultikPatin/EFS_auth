import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.configs.postgres import PostgresSettings
from src.core.db.clients.abstract import AbstractDBClient

sqlalchemy_echo = os.getenv("SQLALCHEMY_ECHO", "True") == "True"

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG

settings = PostgresSettings(
    _env_file="./infra/var/auth/.env.postgres",
    _env_file_encoding="utf-8",
)


class PostgresDatabase(AbstractDBClient):
    def __init__(self, settings: PostgresSettings) -> None:
        self._async_session_factory = async_sessionmaker(
            create_async_engine(
                settings.postgres_connection_url, echo=sqlalchemy_echo
            )
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        try:
            logger.debug("==> Session open")
            session = self._async_session_factory()
            yield session
        except Exception as error:
            logger.exception("==> Session rollback because of exception", error)
            await session.rollback()
            raise
        finally:
            logger.debug("==> Session close")
            await session.close()


def get_postgres_db() -> PostgresDatabase:
    return PostgresDatabase(settings)
