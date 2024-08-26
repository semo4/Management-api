from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ProjectsResponse(BaseModel):
    id: UUID
    name: str
    section_id: Optional[UUID | None] = ""
    section_name: Optional[str | None] = ""
    place: str
    description: str
    start_date: datetime
    end_date: datetime
    project_evaluation: float
    project_revenue: float
    project_depth: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProjectsRequest(BaseModel):
    name: Optional[str] = Field(
        pattern=r"[A-Za-z]{5,50}",
        description="Name must be all character at least with length of 5",
    )
    section_id: Optional[UUID]
    place: Optional[str] = Field(
        pattern=r"[A-Za-z]{5,50}",
        description="profession must be all character at least with length of 5",
    )
    description: Optional[str] = Field(
        pattern=r"[A-Za-z]{5,50}",
        description="profession must be all character at least with length of 5",
    )
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    project_evaluation: Optional[float] = 0
