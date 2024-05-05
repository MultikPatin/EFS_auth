from typing import Any

from fastapi import Depends, HTTPException, status
from jwt import (
    ExpiredSignatureError,
    InvalidSignatureError,
    decode,
    get_unverified_header,
)

from src.auth.core.config import settings
from src.core.oauth_clients.google import OauthGoogle, get_google


async def validate_token(
    token, oauth_client: OauthGoogle = Depends(get_google)
) -> Any:
    header_data = get_unverified_header(token)
    internal_token_secret = settings.auth_jwt.authjwt_secret_key

    try:
        raw_jwt = decode(
            token,
            key=internal_token_secret,
            key=settings.authjwt_secret_key,
            algorithms=[
                header_data["alg"],
            ],
        )
    except (InvalidSignatureError, ExpiredSignatureError) as e:
        raise HTTPException(
            status_code=status.UNAUTHORIZED,
            detail=f"{e}: invalid token",
        ) from None
    # return raw_jwt
