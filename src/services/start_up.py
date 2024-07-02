import logging

from uuid import UUID

from sqlalchemy import select, text

from src.configs import StartUpSettings
from src.models.api.v1.roles import RequestRoleCreate
from src.models.api.v1.users import RequestUserCreate
from src.db.clients.postgres import PostgresDatabase
from src.db.entities import Role, User

logger = logging.getLogger("StartUpService")


class StartUpService:
    def __init__(self, database: PostgresDatabase, settings: StartUpSettings):
        self.__database = database
        self.__settings = settings

    async def create_empty_role(self) -> None:
        role_uuid = await self.get_uuid_by_name(self.__settings.empty_role_name)
        if role_uuid:
            return
        logger.info("Role with name %s already exist", self.__settings.empty_role_name)
        await self.create_role(
            RequestRoleCreate(
                name=self.__settings.empty_role_name,
                description=self.__settings.empty_role_description,
            )
        )
        logger.info("Created empty role with name %s", self.__settings.empty_role_name)

    async def create_admin_user(self) -> None:
        user_uuid = await self.get_uuid_by_email(self.__settings.admin_email)
        if user_uuid:
            return
        logger.info("User with email %s already exist", self.__settings.admin_email)
        await self.create_user(
            RequestUserCreate(
                email=self.__settings.admin_email,
                password=self.__settings.admin_password,
                first_name=None,
                last_name=None,
            )
        )
        logger.info("Created admin user with email %s", self.__settings.admin_email)

    async def get_uuid_by_name(self, name: str) -> UUID | None:
        async with self.__database.get_session() as session:
            db_obj = await session.execute(select(Role.uuid).where(Role.name == name))
            obj_uuid = db_obj.scalars().first()
            return obj_uuid

    async def get_uuid_by_email(self, email: str) -> UUID | None:
        async with self.__database.get_session() as session:
            db_obj = await session.execute(select(User.uuid).where(User.email == email))
            obj_uuid = db_obj.scalars().first()
            return obj_uuid

    async def create_role(self, instance: RequestRoleCreate) -> None:
        async with self.__database.get_session() as session:
            db_obj = Role(**instance.dict())
            session.add(db_obj)
            await session.commit()

    async def create_user(self, instance: RequestUserCreate) -> None:
        async with self.__database.get_session() as session:
            role_uuid = await self.get_uuid_by_name(self.__settings.empty_role_name)
            instance_dict = instance.dict()
            instance_dict["is_superuser"] = True
            instance_dict["role_uuid"] = role_uuid
            db_obj = User(**instance_dict)
            session.add(db_obj)
            await session.commit()

    async def create_partition(self) -> None:
        """creating partition by login_history"""
        async with self.__database.get_session() as session:
            await session.execute(
                text(
                    """CREATE SCHEMA IF NOT EXISTS partman;
                    """
                )
            )
            await session.execute(
                text(
                    """CREATE EXTENSION IF NOT EXISTS pg_partman WITH SCHEMA partman;
                    """
                )
            )
            await session.execute(
                text(
                    """DROP TABLE IF EXISTS public.login_history CASCADE ;
                    """
                )
            )
            await session.execute(
                text(
                    """DROP TABLE IF EXISTS public.login_history_template CASCADE ;
                    """
                )
            )
            await session.execute(
                text(
                    """
                    CREATE TABLE IF NOT EXISTS public.login_history (
                        user_uuid uuid NOT NULL,
                        ip_address VARCHAR(64) NOT NULL,
                        user_agent VARCHAR(255) NOT NULL,
                        uuid uuid NOT NULL,
                        created_at timestamp NOT NULL DEFAULT TIMEZONE('utc', now()),
                        updated_at timestamp NOT NULL DEFAULT TIMEZONE('utc', now())
                    ) PARTITION BY RANGE (created_at);
                    """
                )
            )
            await session.execute(
                text(
                    """
                    CREATE INDEX ON public.login_history (created_at);
                    """
                )
            )
            await session.execute(
                text(
                    """CREATE TABLE IF NOT EXISTS public.login_history_template (LIKE public.login_history);
                    """
                )
            )
            await session.execute(
                text(
                    """ALTER TABLE public.login_history_template ADD PRIMARY KEY (uuid);
                    """
                )
            )
            await session.execute(
                text(
                    """ALTER TABLE public.login_history_template ADD FOREIGN KEY (user_uuid) REFERENCES public.users (uuid);
                    """
                )
            )
            await session.execute(
                text(
                    """
                    TRUNCATE partman.part_config_sub CASCADE;
                    """
                )
            )
            await session.execute(
                text(
                    """
                    TRUNCATE partman.part_config CASCADE;
                    """
                )
            )
            await session.execute(
                text(
                    """
                    SELECT partman.create_parent(
                        p_parent_table := 'public.login_history',
                        p_control := 'created_at',
                        p_interval := '30 day',
                        p_template_table := 'public.login_history_template'
                    );
                    """
                )
            )
            await session.commit()
