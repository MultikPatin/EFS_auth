from pydantic import Field

from src.utils.settings import ServiceSettings


class SentrySettings(ServiceSettings):
    """
    This class is used to store the notification api connection settings.
    """

    dsn: str = Field(..., alias="SENTRY_DSN")
