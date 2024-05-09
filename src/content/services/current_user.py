from http import HTTPStatus

# from async_fastapi_jwt_auth import AuthJWT
# from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.content.models.api.v1.role import ResponsePermission, ResponseRole
from src.content.validators.token import validate_token

# from src.core.db.repositories.user import UserRepository, get_user_repository
from src.core.db.repositories.role import RoleRepository, get_role_repository

# auth_dep = AuthJWTBearer()


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
        role_repository: RoleRepository,
        # authorize: AuthJWT,
    ):
        self._role_repository = role_repository
        # self._authorize = authorize

    # async def get_me(self, request: Request) -> ResponseUser:
    async def get_permissions(self, role_uuid: str) -> list[ResponsePermission]:
        obj = await self._role_repository.get_with_permissions(role_uuid)
        if not obj:
            return
        model = ResponseRole.model_validate(obj, from_attributes=True)
        return model.permissions


def get_current_user(
    role_repository: RoleRepository = Depends(get_role_repository),
    # authorize: AuthJWT = Depends(auth_dep),
) -> CurrentUserService:
    return CurrentUserService(role_repository)
