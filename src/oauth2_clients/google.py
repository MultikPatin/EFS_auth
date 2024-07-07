import logging

from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.jose import JWTClaims, jwt
from authlib.oidc.core import CodeIDToken
from authlib.oauth2.auth import OAuth2Token

from src.configs import Oauth2GoogleSettings
from src.oauth2_clients.abstract import AbstractModelOauth2Client

logger = logging.getLogger("Oauth2GoogleClient")


class Oauth2GoogleClient(AbstractModelOauth2Client):
    """
    Клиент для работы api с Google oauth2.

    Args:
        client (AsyncOAuth2Client): объект для работы с Google oauth2
        settings (Oauth2GoogleSettings): настройки клиента
    """

    def __init__(self, client: AsyncOAuth2Client, settings: Oauth2GoogleSettings):
        self.__client = client
        self.__settings = settings

    async def create_authorization_url(self) -> str:
        """
        Создать url для авторизации Google.

        Returns:
            valid_authorization_url (str): url для авторизации Google.
        """
        authorization_url, _ = self.__client.create_authorization_url(
            url=self.__settings.config_dict.get("authorization_endpoint"),
            state=self.__settings.state.get_secret_value(),
        )
        return authorization_url + "&access_type=offline"

    async def fetch_token(
        self, authorization_response: str
    ) -> dict[str, str] | OAuth2Token:
        """
        Получить токены из Google response url.

        Args:
            authorization_response (str): Google response url.

        Returns:
            response (dict): Google response, содержащий токены.
        """
        return await self.__client.fetch_token(
            url=self.__settings.config_dict.get("token_endpoint"),
            authorization_response=authorization_response,
        )

    async def get_claims(self, jwt_token: str) -> JWTClaims:
        """
        Получить информацию о пользователе из jwt_token.

        Args:
            jwt_token (str): Google jwt_token, содержащий информацию о пользователе.

        Returns:
            claims (JWTClaims): Информация о пользователе.
        """
        jwks_uri = self.__settings.config_dict.get("jwks_uri")
        try:
            keys_response = await self.__client.get(jwks_uri)
        except Exception as error:
            logger.error(
                "Error get request with key `%s:`: %s.",
                jwks_uri,
                error,
            )
            raise
        claims = jwt.decode(jwt_token, keys_response.json(), claims_cls=CodeIDToken)
        claims.validate()
        return claims


oauth2_google_client: Oauth2GoogleClient | None = None


async def get_oauth2_google_client() -> Oauth2GoogleClient | None:
    return oauth2_google_client
