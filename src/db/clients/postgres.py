import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.configs import PostgresSettings

logger = logging.getLogger("PostgresDatabase")


class PostgresDatabase:
    def __init__(self, settings: PostgresSettings) -> None:
        self._async_session_factory = async_sessionmaker(
            create_async_engine(
                settings.postgres_connection_url, echo=settings.sqlalchemy_echo
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


def get_postgres_db(
    settings: PostgresSettings = PostgresSettings(),
) -> PostgresDatabase:
    return PostgresDatabase(settings)
