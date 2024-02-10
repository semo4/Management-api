from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class CovenantsCashResponse(BaseModel):
    id: UUID
    name: str
    partner_id: Optional[UUID | None] = ''
    partner_name: Optional[str | None] = ''
    price: float
    date: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CovenantsCashRequest(BaseModel):
    name: Optional[str] = Field(pattern=r'[A-Za-z]{5,50}',
                                description='Name must be all character at least with length of 5')
    partner_id: Optional[UUID] = ''
    price: Optional[float] = 0
    date: Optional[datetime] = None


class CovenantsDevicesResponse(BaseModel):
    id: UUID
    title: str
    worker_id: Optional[UUID | None] = ''
    worker_name: Optional[str | None] = ''
    desc: str
    date: datetime


class CovenantsDevicesRequest(BaseModel):
    title: Optional[str] = Field(pattern=r'[A-Za-z]{5,50}',
                                 description='Name must be all character at least with length of 5')
    worker_id: Optional[UUID] = ''
    desc: Optional[str] = Field(pattern=r'[A-Za-z]{5,50}',
                                description='Name must be all character at least with length of 5')
    date: Optional[datetime] = None
