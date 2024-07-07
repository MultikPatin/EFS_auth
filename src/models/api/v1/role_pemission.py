from uuid import UUID

from pydantic import BaseModel


class RequestRolePermissionCreate(BaseModel):
    role_uuid: UUID
    permission_uuid: UUID
