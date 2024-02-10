from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class OutcomesResponse(BaseModel):
    id: UUID
    buyer_name: str
    amount_payed: float
    project_id: Optional[UUID | None] = ''
    category_id: Optional[UUID | None] = ''
    project_name: Optional[str | None] = ''
    category_name: Optional[str | None] = ''
    reason: Optional[str | None] = ''
    date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class OutcomesRequest(BaseModel):
    # id: UUID = Field(
    #     pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$", description='UUID it is unique value for each row')

    buyer_name: str = Field(pattern=r'[A-Za-z]{5,50}',
                            description='Store Name must be all character at least with length of 5')
    amount_payed: float
    project_id: Optional[UUID | None] = ''
    category_id: Optional[UUID | None] = ''
    reason: Optional[str | None] = ''
    date: Optional[datetime] = None
