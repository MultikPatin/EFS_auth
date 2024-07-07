import json
from typing import Any
from urllib.request import urlretrieve
from pydantic import SecretStr
from pydantic.fields import Field

from src.utils.settings import EnvSettings, BASE_DIR


class Oauth2GoogleSettings(EnvSettings):
    """
    This class is used to store the Google oauth2 client settings.
    """

    client_id: str = Field(..., alias="OAUTH2_GOOGLE_CLIENT_ID")
    client_secret: str = Field(..., alias="OAUTH2_GOOGLE_CLIENT_SECRET")
    scope: str = Field(default="openid email profile", alias="OAUTH2_GOOGLE_SCOPE")
    redirect_uri: str = Field(..., alias="OAUTH2_GOOGLE_REDIRECT_URI")
    prompt: str = Field(..., alias="OAUTH2_GOOGLE_PROMPT")
    config_url: str = Field(..., alias="OAUTH2_GOOGLE_CONFIG_URL")
    state: SecretStr = Field(..., alias="OAUTH2_GOOGLE_STATE")

    @property
    def config_dict(self) -> dict[str, Any]:
        file_name = self.config_url.split("/")[2]
        file_path = f"{BASE_DIR}/src/configs/{file_name}"
        urlretrieve(self.config_url, file_path)
        with open(file_path) as json_file:
            return json.load(json_file)

    @property
    def settings_dict(self) -> dict[str, Any]:
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self.scope,
            "redirect_uri": self.redirect_uri,
            "prompt": self.prompt,
        }
