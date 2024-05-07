from functools import lru_cache
from http import HTTPStatus

from fastapi import Depends, HTTPException, Request

from src.auth.core.config import settings
from src.auth.models.api.v1.social_account import RequestSocialAccount
from src.auth.models.api.v1.users import RequestUserCreate
from src.auth.models.db.user import UserDB
from src.core.cache.redis import RedisCache, get_redis
from src.core.db.repositories.login_history import (
    LoginHistoryRepository,
    get_login_history_repository,
)
from src.core.db.repositories.social_account import (
    SocialAccountRepository,
    get_social_account,
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
        social_account_repository: SocialAccountRepository,
    ):
        self._cache = cache
        self._oauth_client = oauth_client
        self._user_repository = user_repository
        self._history_repository = history_repository
        self._social_account_repository = social_account_repository

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
        social_name = claims.get("iss")
        social_id = claims.get("sub")
        email = claims.get("email")
        user_uuid = await self._social_account_repository.get_by_social_name_id(
            social_name, social_id
        )
        if not user_uuid:
            credentials_needed = RequestUserCreate(
                email=email,
                password="12345678aaaasfds",
                first_name=claims.get("given_name"),
                last_name="family_name",
            )
            obj = await self._user_repository.create(credentials_needed)
            user = UserDB.model_validate(obj, from_attributes=True)
            await self._social_account_repository.create(
                RequestSocialAccount(
                    user_uuid=user.uuid,
                    social_name=social_name,
                    social_id=social_id,
                )
            )
            user_uuid = user.uuid

        print(f"\n{access_token=}\n")
        print(f"\n{refresh_token=}\n")
        print(f"\n{social_name=}\n")
        print(f"\n{social_id=}\n")
        print(f"\n{email=}\n")
        print(f"\n{user_uuid=}\n")
        return claims


@lru_cache
def get_oauth2_service(
    cache: RedisCache = Depends(get_redis),
    oauth_client: OauthGoogle = Depends(get_google),
    user_repository: UserRepository = Depends(get_user_repository),
    history_repository: LoginHistoryRepository = Depends(
        get_login_history_repository
    ),
    social_account_repository: SocialAccountRepository = Depends(
        get_social_account
    ),
) -> OAuth2Service:
    return OAuth2Service(
        cache,
        oauth_client,
        user_repository,
        history_repository,
        social_account_repository,
    )
