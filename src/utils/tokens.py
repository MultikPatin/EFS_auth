from datetime import datetime, timedelta
from functools import lru_cache

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from fastapi import Depends

from src.cache.redis import RedisCache, get_redis
from src.configs import TokenSettings
from src.models.token import CacheTokens, UserClaims


class TokenUtils:
    def __init__(
        self,
        cache: RedisCache,
        authorize: AuthJWT,
        settings: TokenSettings,
    ):
        self.__cache = cache
        self.__authorize = authorize
        self.__settings = settings

    async def delete_oldest_token_if_necessary(self, user_uuid: str) -> None:
        # TODO Возможно ли лучше?)
        tokens = await self.__cache.get_tokens(user_uuid)
        if not tokens:
            return
        if len(tokens) >= self.__settings.user_max_sessions:
            oldest = datetime.max
            oldest_token = tokens[0]
            for token in tokens:
                user_claims = await self.__authorize.get_raw_jwt(token)
                token_end = datetime.fromtimestamp(user_claims.get("exp"))
                if oldest > token_end:
                    oldest = token_end
                    oldest_token = token

            await self.__cache.delete_tokens(user_uuid, oldest_token)

    async def unset_tokens_from_cookies(
        self, access: bool = False, refresh: bool = False
    ) -> None:
        if access:
            await self.__authorize.unset_access_cookies()
        if refresh:
            await self.__authorize.unset_refresh_cookies()

    async def set_tokens_to_cookies(self, tokens: CacheTokens) -> None:
        if tokens.access:
            await self.__authorize.set_access_cookies(tokens.access)
        if tokens.refresh:
            await self.__authorize.set_refresh_cookies(tokens.refresh)

    async def create_tokens(self, user_claims: UserClaims) -> CacheTokens:
        new_access_token = await self.__authorize.create_access_token(
            subject=user_claims.user_uuid, user_claims=user_claims.model_dump()
        )
        new_refresh_token = await self.__authorize.create_refresh_token(
            subject=user_claims.user_uuid,
            expires_time=timedelta(self.__settings.expire_time_in_minutes),
            user_claims=user_claims.model_dump(),
        )
        return CacheTokens(access=new_access_token, refresh=new_refresh_token)

    async def base_login(self, user_claims: UserClaims) -> None:
        tokens = await self.create_tokens(user_claims)
        await self.set_tokens_to_cookies(tokens)
        await self.delete_oldest_token_if_necessary(user_claims.user_uuid)
        await self.__cache.set_token(user_claims.user_uuid, tokens.refresh)
        # TODO Нотификация с логирование пользователя


@lru_cache
def get_token_utils(
    cache: RedisCache = Depends(get_redis),
    authorize: AuthJWT = AuthJWTBearer(),
    settings: TokenSettings = TokenSettings(),
) -> TokenUtils:
    return TokenUtils(cache, authorize, settings)
