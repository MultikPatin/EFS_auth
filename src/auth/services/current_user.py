from http import HTTPStatus

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.models.api.v1.users import ResponseUser
from src.auth.validators.token import validate_token
from src.core.db.repositories.user import UserRepository, get_user_repository


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
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
        decoded_token = self.parse_token(credentials.credentials)
        if not decoded_token:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Invalid or expired token.",
            )
        return decoded_token

    @staticmethod
    def parse_token(jwt_token: str) -> dict[str, str] | None:
        return validate_token(jwt_token)


security_jwt = JWTBearer()


class CurrentUserService:
    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self._user_repository = user_repository

    async def get_me(self, user_uuid: str) -> ResponseUser:
        obj = await self._user_repository.get(user_uuid)
        if not obj:
            return
        model = ResponseUser.model_validate(obj, from_attributes=True)
        return model

    async def is_superuser(self, user_uuid: str):
        user = await self.get_me(user_uuid)
        if not user.is_superuser:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="You do not have sufficient "
                "permissions to perform this action.",
            )


def get_current_user(
    user_repository: UserRepository = Depends(get_user_repository),
) -> CurrentUserService:
    return CurrentUserService(user_repository)
