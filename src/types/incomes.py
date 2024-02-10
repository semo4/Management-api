from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class IncomesResponse(BaseModel):
    id: UUID
    project_id: Optional[UUID | None] = ''
    section_id: Optional[UUID | None] = ''
    section_name: Optional[str | None] = ''
    project_name: Optional[str | None] = ''
    receiving_person: str
    gave_person: str
    check_number: int = 0
    payment_number: int = 0
    amount: Optional[float] = 0
    way_of_receiving: Optional[str | None] = ''
    description: Optional[str | None] = ''
    receiving_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class IncomesRequest(BaseModel):
    # id: UUID = Field(
    #     pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$", description='UUID it is unique value for each row')

    project_id: Optional[UUID | None] = ''
    section_id: Optional[UUID | None] = ''
    receiving_person: str = Field(pattern=r'[A-Za-z]{5,50}',
                                  description='Store Name must be all character at least with length of 5')
    gave_person: str = Field(pattern=r'[A-Za-z]{5,50}',
                             description='Store Name must be all character at least with length of 5')
    check_number: Optional[int] = 0
    payment_number: Optional[int] = 0
    amount: Optional[float] = 0
    way_of_receiving: Optional[str | None] = ''
    description: Optional[str | None] = ''
    receiving_date: Optional[datetime] = None
