from pydantic import Field, SecretStr


from src.utils.settings import FastApiSettings


class StartUpSettings(FastApiSettings):
    empty_role_name: str = Field(..., alias="EMPTY_ROLE_NAME")
    empty_role_description: str = Field(..., alias="EMPTY_ROLE_DESCRIPTION")
    admin_email: str = Field(..., alias="ADMIN_EMAIL")
    admin_password: SecretStr = Field(..., alias="ADMIN_PASSWORD")
