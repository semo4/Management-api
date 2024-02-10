from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class WithdrawContractorsResponse(BaseModel):
    id: UUID
    section_id: Optional[UUID | None] = ''
    project_id: Optional[UUID | None] = ''
    contractor_id: Optional[UUID | None] = ''
    section_name: Optional[str | None] = ''
    project_name: Optional[str | None] = ''
    contractor_name: Optional[str | None] = ''
    amount: Optional[float] = 0
    date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class WithdrawContractorsRequest(BaseModel):
    section_id: Optional[UUID | None] = ''
    project_id: Optional[UUID | None] = ''
    contractor_id: Optional[UUID | None] = ''
    amount: Optional[float] = 0
    date: Optional[datetime] = None
