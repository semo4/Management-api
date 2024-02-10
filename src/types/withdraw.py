from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class WithdrawResponse(BaseModel):
    id: UUID
    section_id: Optional[UUID | None] = ''
    project_id: Optional[UUID | None] = ''
    partner_id: Optional[UUID | None] = ''
    section_name: Optional[str | None] = ''
    project_name: Optional[str | None] = ''
    partner_name: Optional[str | None] = ''
    amount: Optional[float] = 0
    date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class WithdrawRequest(BaseModel):
    section_id: Optional[UUID | None] = ''
    project_id: Optional[UUID | None] = ''
    partner_id: Optional[UUID | None] = ''
    amount: Optional[float] = 0
    date: Optional[datetime] = None
