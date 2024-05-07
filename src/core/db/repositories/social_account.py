from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select

# from src.auth.models.api.v1.users import RequestUserCreate, RequestUserUpdate
from src.auth.models.api.v1.social_account import RequestSocialAccount
from src.core.db.clients.postgres import PostgresDatabase, get_postgres_db
from src.core.db.entities import SocialAccount
from src.core.db.repositories.base import (
    InitRepository,
)


class SocialAccountRepository(InitRepository):
    # def __init__(
    #     self,
    #     database: PostgresDatabase,
    #     model: type[SocialAccount],
    #     user_repository: UserRepository,
    # ):
    #     super().__init__(database, model)
    #     self.user_repository = user_repository

    async def create(self, instance: RequestSocialAccount) -> SocialAccount:
        async with self._database.get_session() as session:
            # role_uuid = await self.role_repository.get_uuid_by_name(
            #     settings.empty_role_name
            # )
            # create_dict = instance.dict()
            # create_dict["role_uuid"] = role_uuid
            db_obj = self._model(**instance.model_dump())
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def get_by_social_name_id(
        self, social_name: str, social_id: str
    ) -> UUID | None:
        async with self._database.get_session() as session:
            db_obj = await session.execute(
                select(self._model.user_uuid).where(
                    self._model.social_name == social_name
                    and self._model.social_id == social_id
                )
            )
            obj_uuid = db_obj.scalars().first()
            return obj_uuid

    # async def get_with_role(self, user_uuid: UUID) -> Any | None:
    #     async with self._database.get_session() as session:
    #         db_obj = await session.execute(
    #             select(self._model)
    #             .where(self._model.uuid == user_uuid)
    #             .options(joinedload(self._model.role))
    #         )
    #         return db_obj.unique().scalars().first()

    # async def change_password(
    #     self, user_uuid: UUID, obj: RequestPasswordChange
    # ) -> User | None:
    #     async with self._database.get_session() as session:
    #         user = await self.get(user_uuid)
    #         if user.check_password(obj.current_password.get_secret_value()):
    #             user.password = obj.new_password.get_secret_value()
    #             session.add(user)
    #             await session.commit()
    #             await session.refresh(user)
    #             return user
    #         return None

    # async def change_user_role(self, user_uuid: UUID, role_uuid: UUID) -> Any:
    #     async with self._database.get_session() as session:
    #         user = await self.get(user_uuid)
    #         user.role_uuid = role_uuid
    #         session.add(user)
    #         await session.commit()
    #         return await self.get_with_role(user_uuid)


@lru_cache
def get_social_account(
    database: PostgresDatabase = Depends(get_postgres_db),
    # user_repository: UserRepository = Depends(get_user_repository),
) -> SocialAccountRepository:
    return SocialAccountRepository(database, SocialAccount)
