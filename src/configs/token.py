from pydantic import Field

from src.configs.authjwt import AuthJWTSettings


class TokenSettings(AuthJWTSettings):
    expire_time_in_minutes: int = Field(..., alias="TOKEN_EXPIRE_TIME_IN_MINUTES")
    user_max_sessions: int = Field(..., alias="USER_MAX_SESSIONS")
