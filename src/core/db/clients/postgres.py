import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TypeVar

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.configs.postgres import (
    PostgresAuthSettings,
    PostgresContentSettings,
    PostgresSettings,
    get_postgres_auth_settings,
    get_postgres_content_settings,
    get_postgres_settings,
)
from src.core.db.clients.abstract import AbstractDBClient

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG

D = TypeVar("D", bound=PostgresSettings)
load_dotenv()


class PostgresDatabase(AbstractDBClient):
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
    settings: PostgresSettings = Depends(get_postgres_settings, use_cache=True),
) -> PostgresDatabase:
    return PostgresDatabase(settings)


def get_postgres_content_db(
    settings: PostgresContentSettings = Depends(
        get_postgres_content_settings, use_cache=True
    ),
) -> PostgresDatabase:
    return PostgresDatabase(settings)


def get_postgres_auth_db(
    settings: PostgresAuthSettings = Depends(
        get_postgres_auth_settings, use_cache=True
    ),
) -> PostgresDatabase:
    return PostgresDatabase(settings)
