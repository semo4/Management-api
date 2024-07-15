from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SalariesResponse(BaseModel):
    id: UUID
    project_id: Optional[UUID | None]
    worker_id: Optional[UUID | None]
    section_id: Optional[UUID | None]
    project_name: Optional[str | None] = ""
    worker_name: Optional[str | None] = ""
    section_name: Optional[str | None] = ""
    salary_type: Optional[str | None] = ""
    amount: Optional[float] = 0
    date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class SalariesRequest(BaseModel):
    project_id: Optional[UUID | None]
    worker_id: Optional[UUID | None]
    section_id: Optional[UUID | None]
    salary_type: Optional[str | None] = ""
    amount: Optional[float] = 0
    date: Optional[datetime] = None
