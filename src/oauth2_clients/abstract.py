from abc import ABC, abstractmethod

from authlib.jose import JWTClaims
from authlib.oauth2.auth import OAuth2Token


class AbstractModelOauth2Client(ABC):
    """
    Abstract base class for oauth. Provides an interface for oauth.
    """

    @abstractmethod
    async def create_authorization_url(self) -> None:
        """
        Generate url for oauth authorization.

        Returns:
            valid_authorization_url (str): url for oauth authorization.
        """
        raise NotImplementedError

    @abstractmethod
    async def fetch_token(
        self, authorization_response: str
    ) -> dict[str, str] | OAuth2Token:
        """
        Fetch tokens from oauth response url.

        Args:
            authorization_response (str): Response url.

        Returns:
            response (dict[str, str] | OAuth2Token): Google response with tokens
        """
        raise NotImplementedError

    @abstractmethod
    async def get_claims(self, jwt_token: str) -> JWTClaims:
        """
        Get user info from JWT.

        Args:
            jwt_token (str): Oauth JWT, with user info.

        Returns:
            claims (Any): User info.
        """
        raise NotImplementedError
