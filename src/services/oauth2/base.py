import random
import string
from uuid import UUID

from authlib.jose import JWTClaims

from async_fastapi_jwt_auth import AuthJWT
from fastapi import Request

from pydantic import SecretStr

from src.cache.redis import RedisCache
from src.db.entities import User
from src.models.api.v1.login_history import RequestLoginHistory
from src.models.api.v1.social_account import RequestCreateSocialAccount
from src.models.api.v1.users import RequestUserCreate
from src.models.token import UserClaims
from src.utils.tokens import TokenUtils
from src.db.repositories.login_history import LoginHistoryRepository
from src.db.repositories.social_account import SocialAccountRepository
from src.db.repositories.user import UserRepository


class OAuth2BaseService:
    def __init__(
        self,
        cache: RedisCache,
        user_repository: UserRepository,
        history_repository: LoginHistoryRepository,
        social_account_repository: SocialAccountRepository,
        authorize: AuthJWT,
        token: TokenUtils,
    ):
        self._cache = cache
        self._user_repository = user_repository
        self._history_repository = history_repository
        self._social_account_repository = social_account_repository
        self._authorize = authorize
        self._token = token

    async def checkin_oauth_user(self, claims: JWTClaims | UUID) -> UserClaims:
        if isinstance(claims, UUID):
            user = await self._user_repository.get(claims)
            return self.__get_user_claims(user)
        else:
            password = "".join(
                random.choices(
                    string.digits + string.ascii_letters + string.punctuation,
                    k=20,
                )
            )
            user = await self._user_repository.create(
                RequestUserCreate(
                    email=claims.get("email"),
                    password=SecretStr(password),
                    first_name=claims.get("given_name"),
                    last_name=claims.get("family_name"),
                )
            )
            # TODO Нотификация с просьбой сменить пароль
            await self._social_account_repository.create(
                RequestCreateSocialAccount(
                    user_uuid=user.uuid,
                    social_name=claims.get("iss"),
                    social_id=claims.get("sub"),
                )
            )
            return self.__get_user_claims(user)

    @staticmethod
    def __get_user_claims(user: User | None) -> UserClaims:
        # TODO Возможно ли лучше?)
        try:
            user_claims = UserClaims(
                user_uuid=user.uuid,
                role_uuid=user.email,
            )
        except ValueError:
            pass
        return user_claims

    async def login(self, request: Request, user_claims: UserClaims) -> None:
        await self._token.base_login(user_claims)
        await self._history_repository.create(
            RequestLoginHistory(
                user_uuid=UUID(user_claims.user_uuid),
                ip_address=request.headers.get("Host"),
                user_agent=request.headers.get("User-Agent"),
            )
        )

    async def check_social_account(self, claims: JWTClaims) -> JWTClaims | UUID:
        user_uuid = await self._social_account_repository.get_by_social_name_id(
            social_name=claims.get("iss"), social_id=claims.get("sub")
        )
        return user_uuid if user_uuid else claims
