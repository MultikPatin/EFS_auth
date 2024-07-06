from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from src.models.api.v1 import RequestCreateSocialAccount
from src.db.clients.postgres import PostgresDatabase, get_postgres_db
from src.db.entities import SocialAccount
from src.db.repositories.base import PostgresRepositoryCD


class SocialAccountRepository(
    PostgresRepositoryCD[SocialAccount, RequestCreateSocialAccount]
):
    async def remove(self, instance_uuid: UUID, **kwargs) -> UUID:
        raise NotImplementedError

    async def get_by_social_name_id(
        self, social_name: str, social_id: str
    ) -> str | None:
        async with self._database.get_session() as session:
            db_obj = await session.execute(
                select(self._model.uuid)
                .where(
                    and_(
                        SocialAccount.social_name == social_name,
                        SocialAccount.social_id == social_id,
                    )
                )
                .options(selectinload(SocialAccount.user))
            )
            obj_uuid = db_obj.scalars().first()
            return obj_uuid


@lru_cache
def get_social_account(
    database: PostgresDatabase = Depends(get_postgres_db),
) -> SocialAccountRepository:
    return SocialAccountRepository(database, SocialAccount)
