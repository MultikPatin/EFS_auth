from functools import lru_cache
from http import HTTPStatus

from fastapi import Depends, HTTPException, Request

# from starlette.requests import Request
from src.auth.core.config import settings
from src.core.cache.redis import RedisCache, get_redis
from src.core.db.repositories.login_history import (
    LoginHistoryRepository,
    get_login_history_repository,
)
from src.core.db.repositories.user import UserRepository, get_user_repository
from src.core.oauth_clients.google import OauthGoogle, get_google


class OAuth2Service:
    def __init__(
        self,
        cache: RedisCache,
        oauth_client: OauthGoogle,
        user_repository: UserRepository,
        history_repository: LoginHistoryRepository,
    ):
        self._cache = cache
        self._oauth_client = oauth_client
        self._user_repository = user_repository
        self._history_repository = history_repository

    async def get_authorization_url(self, request: Request) -> str:
        return await self._oauth_client.create_authorization_url()

    async def auth_via_google(self, request: Request):
        if (
            request.query_params.get("state")
            != settings.google.google_state.get_secret_value()
        ):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid state parameter.",
            )

        authorization_response = str(request.url)
        response = await self._oauth_client.fetch_token(authorization_response)

        access_token = response.get("access_token")
        refresh_token = response.get("refresh_token")
        id_token = response.get("id_token")

        claims = await self._oauth_client.get_claims(id_token)

        print(f"\n\n{type(id_token)}\n\n")
        print(f"\n\n{access_token=}\n\n")
        print(f"\n\n{refresh_token=}\n\n")
        print(f"\n\n{id_token=}\n\n")
        print(f"\n\n{claims=}\n\n")
        return claims


@lru_cache
def get_oauth2_service(
    cache: RedisCache = Depends(get_redis),
    oauth_client: OauthGoogle = Depends(get_google),
    user_repository: UserRepository = Depends(get_user_repository),
    history_repository: LoginHistoryRepository = Depends(
        get_login_history_repository
    ),
) -> OAuth2Service:
    return OAuth2Service(
        cache, oauth_client, user_repository, history_repository
    )
