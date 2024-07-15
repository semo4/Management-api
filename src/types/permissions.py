from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SystemAccess(BaseModel):
    permission_types_id: UUID
    permission_types_symbol: str
    system_parts_name: str


class PermissionsResponse(BaseModel):
    id: UUID
    supervise_id: UUID
    approval: bool
    approval_timestamp: Optional[datetime] = None
    system_access: List[SystemAccess] = []
    project_id: UUID
    user_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PermissionsRequest(BaseModel):
    supervise_id: Optional[str] = Field(
        pattern=r"[A-Za-z]{5,50}",
        description="Store Name must be all character at least with length of 5",
    )
    project_id: Optional[UUID | None]
    user_id: Optional[UUID | None]
    supervise_id: Optional[UUID | None]
    approval: Optional[bool | False]
    system_access: Optional[List[SystemAccess] | None]
