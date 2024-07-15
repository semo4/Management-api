from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class OperationsResponse(BaseModel):
    id: UUID
    section_id: Optional[UUID | None]
    project_id: Optional[UUID | None]
    worker_id: Optional[UUID | None]
    work_place_id: Optional[UUID | None]
    section_name: Optional[str | None] = ""
    project_name: Optional[str | None] = ""
    worker_name: Optional[str | None] = ""
    workplace_name: Optional[str | None] = ""
    working_hours: Optional[int] = 0
    payment_amount: Optional[float] = 0
    description: Optional[str] = ""
    operation_add_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class OperationsRequest(BaseModel):
    section_id: Optional[UUID | None]
    project_id: Optional[UUID | None]
    worker_id: Optional[UUID | None]
    work_place_id: Optional[UUID | None]
    working_hours: Optional[int] = 0
    description: Optional[str] = ""
    operation_add_date: Optional[datetime] = None
