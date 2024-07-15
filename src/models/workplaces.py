from sqlalchemy import Column, DateTime, String, Table
from sqlalchemy.dialects.postgresql import UUID

from src.database.database import default_now, metaData, new_uuid, now

workplace = Table(
    "workplace",
    metaData,
    Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False, default=new_uuid
    ),
    Column("title", String, nullable=False),
    Column("created_at", DateTime, nullable=False, **default_now),
    Column("updated_at", DateTime, nullable=False, onupdate=now, **default_now),
)
