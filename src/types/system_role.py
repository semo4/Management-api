from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SystemRoleResponse(BaseModel):
    id: UUID
    title: str
    layer: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class SystemRoleRequest(BaseModel):
    title: str = Field(
        pattern=r"[A-Za-z]{5,50}",
        description="title must be all character at least with length of 5",
    )
