from sqlalchemy import Table, Column, String, DateTime
from src.database.database import metaData, now, default_now, new_uuid
from sqlalchemy.dialects.postgresql import UUID

sections = Table(
    "sections",
    metaData,
    Column('id', UUID(as_uuid=True), primary_key=True,
           nullable=False, default=new_uuid),
    Column('name', String, nullable=False),
    Column('created_at', DateTime, nullable=False, **default_now),
    Column('updated_at', DateTime, nullable=False, onupdate=now,
           **default_now)
)
