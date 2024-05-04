from functools import lru_cache
from http import HTTPStatus

from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.jose import jwt
from authlib.oidc.core import CodeIDToken
from fastapi import Depends, HTTPException
from starlette.requests import Request

from src.auth.core.config import settings
from src.core.cache.redis import RedisCache, get_redis
from src.core.db.repositories.login_history import (
    LoginHistoryRepository,
    get_login_history_repository,
)
from src.core.db.repositories.user import UserRepository, get_user_repository

scope = "openid email profile"
redirect_uri = "https://d6a9-91-108-28-17.ngrok-free.app/auth/v1/oauth2/auth"
google_config = settings.google_config

client = AsyncOAuth2Client(
    settings.google_client_id,
    settings.google_client_secret.get_secret_value(),
    scope=scope,
    redirect_uri=redirect_uri,
    prompt="consent",
)


class OAuth2Service:
    def __init__(
        self,
        cache: RedisCache,
        user_repository: UserRepository,
        history_repository: LoginHistoryRepository,
    ):
        self._cache = cache
        self._user_repository = user_repository
        self._history_repository = history_repository
        self._client = client

    async def get_authorization_url(self, request: Request) -> str:
        authorization_endpoint = google_config.get("authorization_endpoint")
        authorization_url, _ = self._client.create_authorization_url(
            authorization_endpoint,
            state=settings.google_state.get_secret_value(),
        )
        valid_authorization_url = authorization_url + "&access_type=offline"

        return valid_authorization_url

    async def auth_via_google(self, request: Request):
        authorization_response = str(request.url)
        access_token_endpoint = google_config.get("token_endpoint")
        if (
            request.query_params.get("state")
            != settings.google_state.get_secret_value()
        ):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid state parameter.",
            )
        response = await self._client.fetch_token(
            access_token_endpoint, authorization_response=authorization_response
        )
        access_token = response.get("access_token")
        refresh_token = response.get("refresh_token")
        id_token = response.get("id_token")
        keys_response = await self._client.get(google_config.get("jwks_uri"))
        keys = keys_response.json()
        claims = jwt.decode(id_token, keys, claims_cls=CodeIDToken)
        claims.validate()

        print(f"\n\n{access_token=}\n\n")
        print(f"\n\n{refresh_token=}\n\n")
        print(f"\n\n{id_token=}\n\n")
        print(f"\n\n{claims=}\n\n")
        return claims


@lru_cache
def get_oauth2_service(
    cache: RedisCache = Depends(get_redis),
    user_repository: UserRepository = Depends(get_user_repository),
    history_repository: LoginHistoryRepository = Depends(
        get_login_history_repository
    ),
) -> OAuth2Service:
    return OAuth2Service(cache, user_repository, history_repository)
