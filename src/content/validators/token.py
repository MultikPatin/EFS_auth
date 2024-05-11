from http import HTTPStatus

from fastapi import HTTPException
from jwt import (
    DecodeError,
    ExpiredSignatureError,
    InvalidSignatureError,
    decode,
)

# jwt.exceptions.DecodeError
from src.content.core.config import settings


def validate_token(token) -> dict[str, str] | None:
    try:
        raw_jwt = decode(
            token,
            key=settings.authjwt_secret_key,
            algorithms=settings.authjwt_algorithm,
        )
    except (InvalidSignatureError, ExpiredSignatureError, DecodeError) as e:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"{e}: invalid token",
        ) from None
    return raw_jwt
