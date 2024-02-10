from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class OutcomesCategoriesResponse(BaseModel):
    id: UUID
    title: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class OutcomesCategoriesRequest(BaseModel):
    title: str = Field(pattern=r'[A-Za-z]{5,50}',
                       description='Title must be all character at least with length of 5')
