import os

# from dotenv import load_dotenv
from pydantic.fields import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# load_dotenv(".env")
local = os.getenv("LOCAL", "True")


class RedisSettings(BaseSettings):
    """
    This class is used to store the REDIS connection settings.
    """

    model_config = SettingsConfigDict(extra="ignore")
    host: str = Field(..., alias="REDIS_HOST")
    port: int = Field(..., alias="REDIS_PORT")

    def __correct_host(self) -> str:
        if local == "True":
            return "localhost"
        return self.host

    @property
    def connection_dict(self) -> dict:
        return {
            "host": self.__correct_host(),
            "port": self.port,
        }
