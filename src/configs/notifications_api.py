from pydantic import Field

from src.utils.settings import ServiceSettings


class NotificationApiSettings(ServiceSettings):
    """
    This class is used to store the notification api connection settings.
    """

    host: str = Field(..., alias="NOTIFICATION_API_HOST")
    port: int = Field(..., alias="NOTIFICATION_API_PORT")
    host_local: str = Field(default="localhost", alias="NOTIFICATION_API_HOST_LOCAL")
    port_local: int = Field(default=8000, alias="NOTIFICATION_API_PORT_LOCAL")
