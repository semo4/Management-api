from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ContractorsResponse(BaseModel):
    id: UUID
    name: str
    section_id: Optional[UUID | None]
    project_id: Optional[UUID | None]
    section_name: Optional[str | None] = ""
    project_name: Optional[str | None] = ""
    amount: Optional[float] = 0
    paid_amount: Optional[float] = 0
    rest_amount: Optional[float] = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ContractorsRequest(BaseModel):
    # id: UUID = Field(
    #     pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$", description='UUID it is unique value for each row')
    name: str = Field(
        pattern=r"[A-Za-z]{5,50}",
        description="Store Name must be all character at least with length of 5",
    )
    project_id: Optional[UUID | None]
    section_id: Optional[UUID | None]
    amount: Optional[float] = 0
    paid_amount: Optional[float] = 0
