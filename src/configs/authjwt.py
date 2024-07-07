from pydantic import Field

from src.utils.settings import EnvSettings


class AuthJWTSettings(EnvSettings):
    authjwt_secret_key: str = Field(..., alias="AUTHJWT_SECRET_KEY")
    authjwt_algorithm: str = Field(default="HS256", alias="AUTHJWT_ALGORITHM")
    authjwt_token_location: set[str] = Field(default={"cookies"})
    authjwt_cookie_csrf_protect: bool = Field(
        default=True, alias="AUTHJWT_COOKIE_CSRF_PROTECT"
    )
    authjwt_cookie_secure: bool = Field(default=True, alias="AUTHJWT_COOKIE_SECURE")
