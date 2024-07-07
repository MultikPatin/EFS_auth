from http import HTTPStatus

from fastapi import HTTPException
from jwt import (
    ExpiredSignatureError,
    InvalidSignatureError,
    decode,
)

from src.configs import settings


def validate_token(token: str | bytes) -> dict[str, str] | None:
    try:
        raw_jwt = decode(
            jwt=token,
            key=settings.token.authjwt_secret_key,
            algorithms=[settings.token.authjwt_algorithm],
        )
    except (InvalidSignatureError, ExpiredSignatureError) as e:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"{e}: invalid token",
        ) from None
    return raw_jwt
