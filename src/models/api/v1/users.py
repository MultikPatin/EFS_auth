from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from src.models.api.v1.base import (
    LoginMixin,
    TimeMixin,
    UUIDMixin,
)
from src.models.api.v1.roles import ResponseRoleShort
from src.utils.pagination import PaginatedMixin


class RequestUserUpdate(BaseModel):
    first_name: str | None = Field(
        description="Имя пользователя",
        examples=["Вася"],
        min_length=1,
        max_length=64,
    )
    last_name: str | None = Field(
        description="Фамилия пользователя",
        examples=["Пупкин"],
        min_length=1,
        max_length=64,
    )


class RequestUserCreate(RequestUserUpdate, LoginMixin):
    pass


class UserBase(RequestUserCreate, UUIDMixin, TimeMixin):
    is_superuser: bool


class ResponseUser(RequestUserUpdate, UUIDMixin, TimeMixin):
    email: EmailStr = Field(
        description="Email пользователя",
        examples=["exemple@mail.ru"],
        min_length=1,
        max_length=64,
    )
    is_superuser: bool = Field(
        description="Флаг - является ли пользователь администратором",
        examples=[False],
    )
    role_uuid: UUID | None


class ResponseUserShort(RequestUserUpdate, UUIDMixin):
    email: EmailStr = Field(
        description="Email пользователя",
        examples=["exemple@mail.ru"],
        min_length=1,
        max_length=64,
    )


class ResponseUsersPaginated(PaginatedMixin):
    users: list[ResponseUser]


class ResponseUserExtended(ResponseUserShort):
    role: ResponseRoleShort
