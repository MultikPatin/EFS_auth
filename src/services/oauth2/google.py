import logging

from functools import lru_cache
from http import HTTPStatus

from authlib.jose import JWTClaims

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from fastapi import Depends, HTTPException, Request

from src.cache.redis import RedisCache, get_redis
from src.configs import Oauth2GoogleSettings

from src.models.token import UserClaims
from src.oauth2_clients.google import Oauth2GoogleClient, get_oauth2_google_client
from src.services.oauth2.base import OAuth2BaseService
from src.utils.tokens import TokenUtils, get_token_utils
from src.db.repositories.login_history import (
    LoginHistoryRepository,
    get_login_history_repository,
)
from src.db.repositories.social_account import (
    SocialAccountRepository,
    get_social_account,
)
from src.db.repositories.user import UserRepository, get_user_repository

logger = logging.getLogger("GoogleOAuth2Service")


class OAuth2GoogleService(OAuth2BaseService):
    def __init__(
        self,
        cache: RedisCache,
        client: Oauth2GoogleClient,
        user_repository: UserRepository,
        history_repository: LoginHistoryRepository,
        social_account_repository: SocialAccountRepository,
        authorize: AuthJWT,
        token: TokenUtils,
        settings: Oauth2GoogleSettings,
    ):
        super().__init__(
            cache,
            user_repository,
            history_repository,
            social_account_repository,
            authorize,
            token,
        )
        self.__client = client
        self.__settings = settings

    async def get_google_authorization_url(self) -> str:
        return await self.__client.create_authorization_url()

    async def auth_via_google(self, request: Request) -> JWTClaims | UserClaims:
        if (
            request.query_params.get("state")
            != self.__settings.state.get_secret_value()
        ):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid state parameter.",
            )

        response = await self.__client.fetch_token(str(request.url))

        return await self.check_social_account(
            await self.__client.get_claims(str(response.get("id_token")))
        )


@lru_cache
def get_oauth2_google_service(
    cache: RedisCache = Depends(get_redis),
    google_oauth2_client: Oauth2GoogleClient = Depends(get_oauth2_google_client),
    user_repository: UserRepository = Depends(get_user_repository),
    history_repository: LoginHistoryRepository = Depends(get_login_history_repository),
    social_account_repository: SocialAccountRepository = Depends(get_social_account),
    authorize: AuthJWT = AuthJWTBearer(),
    token: TokenUtils = Depends(get_token_utils),
    settings: Oauth2GoogleSettings = Oauth2GoogleSettings(),
) -> OAuth2GoogleService:
    return OAuth2GoogleService(
        cache,
        google_oauth2_client,
        user_repository,
        history_repository,
        social_account_repository,
        authorize,
        token,
        settings,
    )
