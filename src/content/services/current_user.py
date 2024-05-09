import json
from http import HTTPStatus
from json import JSONDecodeError

import aiohttp
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.content.core.config import settings
from src.content.models.api.v1.role import ResponsePermission, ResponseRole
from src.content.validators.token import validate_token


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request
        )
        if not credentials:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Invalid authorization code.",
            )
        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Only Bearer token might be accepted",
            )
        # token = credentials.credentials
        # if not token:
        #     token = request.cookies.get("access_token_cookie")

        # decoded_token = self.parse_token(token)
        decoded_token = self.parse_token(credentials.credentials)
        if not decoded_token:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Invalid or expired token.",
            )
        return decoded_token.get("role_uuid")

    @staticmethod
    def parse_token(jwt_token: str) -> dict[str, str] | None:
        return validate_token(jwt_token)


security_jwt = JWTBearer()


class CurrentUserService:
    def __init__(
        self,
    ): ...
    async def get_permissions(
        self, role_uuid: str, request: Request
    ) -> list[ResponsePermission]:
        url = settings.get_api_roles_url() + f"{role_uuid}/permissions/"

        access_token_cookie = request.cookies.get("access_token_cookie")
        cookies = {
            "access_token_cookie": access_token_cookie,
        }
        async with aiohttp.ClientSession() as session:
            session.cookie_jar.update_cookies(cookies)
            async with session.get(url) as response:
                body = await response.read()
            try:
                body = json.loads(body)
            except JSONDecodeError as e:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=f"{e}: JSON decode error",
                ) from None
        permissions = ResponseRole(
            uuid=body.get("uuid"),
            name=body.get("name"),
            permissions=[
                ResponsePermission(**permission)
                for permission in body.get("permissions")
            ],
        )
        if not permissions:
            return
        return permissions.permissions


def get_current_user() -> CurrentUserService:
    return CurrentUserService()
