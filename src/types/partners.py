from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PartnersResponse(BaseModel):
    id: UUID
    name: str
    section_id: Optional[UUID | None] = ""
    section_name: Optional[str | None] = ""
    amount: float
    pre_amount: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PartnersRequest(BaseModel):
    name: Optional[str] = Field(
        pattern=r"[A-Za-z]{5,50}",
        description="Name must be all character at least with length of 5",
    )
    section_id: Optional[UUID] = ""
    amount: Optional[float] = 0
    pre_amount: Optional[float] = 0
