from pydantic import Field

from src.core.configs.base import ServiceSettings


class RedisSettings(ServiceSettings):
    """
    This class is used to store the REDIS connection settings.
    """

    host: str = Field(..., alias="REDIS_HOST")
    port: int = Field(..., alias="REDIS_PORT")
    host_local: str = Field("localhost", alias="REDIS_HOST_LOCAL")
    port_local: int = Field(6379, alias="REDIS_PORT_LOCAL")

    @property
    def connection_dict(self) -> dict:
        return {
            "host": self.correct_host(),
            "port": self.correct_port(),
        }
