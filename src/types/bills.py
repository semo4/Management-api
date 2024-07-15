from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class BillsResponse(BaseModel):
    id: UUID
    project_id: Optional[UUID | None]
    project_name: Optional[str | None] = ""
    store_name: str
    buyer_name: str
    item: str
    amount: float
    bill_number: int
    bill_picture: Optional[str | None] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class BillsRequest(BaseModel):
    # id: UUID = Field(
    #     pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$", description='UUID it is unique value for each row')
    store_name: Optional[str] = Field(
        pattern=r"[A-Za-z]{5,50}",
        description="Store Name must be all character at least with length of 5",
    )
    project_id: Optional[UUID]
    buyer_name: Optional[str] = ""
    item: Optional[str] = ""
    amount: Optional[float] = 0
    bill_number: Optional[int] = 0
    bill_picture: Optional[str] = ""
