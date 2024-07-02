from pydantic import Field

from src.utils.settings import ServiceSettings


class JaegerSettings(ServiceSettings):
    """
    This class is used to store the JAEGER connection settings.
    """

    host: str = Field(..., alias="JAEGER_HOST")
    port: int = Field(..., alias="JAEGER_PORT")
    host_local: str = Field(default="localhost", alias="JAEGER_HOST_LOCAL")
    port_local: int = Field(default=16686, alias="JAEGER_PORT_LOCAL")
    exporter_agent_host_name: str = Field(
        default="localhost", alias="JAEGER_EXPORTER_AGENT_HOST_NAME"
    )
    exporter_agent_port: int = Field(default=6831, alias="JAEGER_EXPORTER_AGENT_PORT")
