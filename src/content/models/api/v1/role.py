from src.content.models.base import UUIDMixin


class ResponsePermission(UUIDMixin):
    name: str


class ResponseRole(UUIDMixin):
    name: str
    permissions: list[ResponsePermission]
