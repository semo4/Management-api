from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SectionsResponse(BaseModel):
    id: UUID
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class SectionsRequest(BaseModel):
    name: str = Field(
        pattern=r"[A-Za-z]{5,50}",
        description="Name must be all character at least with length of 5",
    )
