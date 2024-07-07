from typing import Annotated
from uuid import UUID

from fastapi import Depends, Path

from src.validators import BaseValidator, DuplicateEmailValidatorMixin
from src.db.repositories.user import UserRepository, get_user_repository


class UserValidator(BaseValidator[UserRepository], DuplicateEmailValidatorMixin):
    pass


def get_user_validator(
    repository: UserRepository = Depends(get_user_repository),
) -> UserValidator:
    return UserValidator(repository)


user_uuid_annotation = Annotated[
    UUID,
    Path(
        alias="user_uuid",
        title="user uuid",
        description="The UUID of the user",
        example="6a0a479b-cfec-41ac-b520-41b2b007b611",
    ),
]
