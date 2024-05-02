import os

# from dotenv import load_dotenv
from pydantic.fields import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# load_dotenv(".env")
local = os.getenv("LOCAL", "True")


class ElasticSettings(BaseSettings):
    """
    This class is used to store the Elastic connection settings.
    """

    model_config = SettingsConfigDict(extra="ignore")
    host: str = Field(..., alias="ELASTIC_HOST")
    port: int = Field(..., alias="ELASTIC_PORT")

    def __correct_host(self) -> str:
        if local == "True":
            return "localhost"
        return self.host

    @property
    def get_host(self) -> str:
        return f"http://{self.__correct_host()}:{self.port}"
