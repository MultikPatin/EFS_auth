from uuid import UUID

from src.models.db.base import BaseMixin


class SocialAccountDB(BaseMixin):
    user_uuid: UUID
    social_name: str | None
    social_id: str | None
