from pydantic import BaseModel, Field

from src.models.api.v1.base import (
    TimeMixin,
    UUIDMixin,
)
from src.utils.pagination import PaginatedMixin


class RequestPermissionUpdate(BaseModel):
    description: str = Field(
        description="Описание разрешения",
        examples=["Новинки сериалов за месяц"],
        min_length=1,
        max_length=255,
    )


class RequestPermissionCreate(RequestPermissionUpdate):
    description: str | None = Field(
        description="Описание разрешения",
        examples=["Новинки сериалов за месяц"],
        min_length=1,
        max_length=255,
    )
    name: str = Field(
        description="Наименование разрешения",
        examples=["Новинки сериалов"],
        min_length=1,
        max_length=64,
    )


class PermissionBase(RequestPermissionUpdate, UUIDMixin, TimeMixin):
    name: str = Field(
        description="Наименование разрешения",
        examples=["Новинки сериалов"],
        min_length=1,
        max_length=64,
    )


class ResponsePermission(RequestPermissionCreate, UUIDMixin, TimeMixin):
    pass


class ResponsePermissionShort(UUIDMixin):
    name: str = Field(
        description="Наименование разрешения",
        examples=["Новинки сериалов"],
        min_length=1,
        max_length=64,
    )


class ResponsePermissionsPaginated(PaginatedMixin):
    permissions: list[ResponsePermissionShort]
