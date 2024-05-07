from uuid import UUID

from pydantic import BaseModel, Field


class RequestSocialAccount(BaseModel):
    user_uuid: UUID = Field(
        description="UUID идентификатор пользователя",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6",
    )
    social_name: str = Field(
        description="Url адрес сервера oauth",
    )
    social_id: str = Field(
        description="Идентификатор пользователя, уникальный среди всех учетных записей сервера oauth",
    )


# class LoginHistoryBase(RequestLoginHistory, UUIDMixin, TimeMixin):
#     pass


# class ResponseLoginHistory(LoginHistoryBase, UUIDMixin, TimeMixin):
#     pass


# class ResponseLoginHistoryPaginated(PaginatedMixin):
#     results: list[ResponseLoginHistory]
