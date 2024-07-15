from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class WorkersResponse(BaseModel):
    id: UUID
    name: str
    profession: str
    daily_amount: float
    total_number_of_working_hours: Optional[int] = 0
    total_payment_amount: Optional[float] = 0
    total_payed_amount: Optional[float] = 0
    rest_amount: Optional[float] = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class WorkersRequest(BaseModel):
    name: Optional[str] = Field(
        pattern=r"[A-Za-z]{5,50}",
        description="Name must be all character at least with length of 5",
    )
    profession: Optional[str] = Field(
        pattern=r"[A-Za-z]{5,50}",
        description="profession must be all character at least with length of 5",
    )
    daily_amount: Optional[float] = 0
