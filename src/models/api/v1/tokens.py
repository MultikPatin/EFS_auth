from pydantic import BaseModel

from src.models.api.v1.base import LoginMixin, TokenMixin


class ResponseToken(BaseModel):
    refresh: str
    access: str


class RequestLogin(LoginMixin):
    pass


class RequestTokenRemover(TokenMixin):
    for_all_sessions: bool


class RequestTokenRefreshChecker(TokenMixin):
    pass


class RequestTokenVerify(TokenMixin):
    access: str
