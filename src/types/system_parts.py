from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SystemPartsResponse(BaseModel):
    id: UUID
    title: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class SystemPartsRequest(BaseModel):
    title: Optional[str] = Field(
        pattern=r"[A-Za-z]{5,50}",
        description="title must be all character at least with length of 5",
    )
