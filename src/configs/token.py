from pydantic import Field

from src.auth.configs.base import ServiceSettings


class RedisSettings(ServiceSettings):
    """
    This class is used to store the REDIS connection settings.
    """

    host: str = Field(..., alias="REDIS_HOST")
    port: int = Field(..., alias="REDIS_PORT")
    host_local: str = Field(..., alias="REDIS_HOST_LOCAL")
    port_local: int = Field(..., alias="REDIS_PORT_LOCAL")
