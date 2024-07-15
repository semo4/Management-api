from sqlalchemy import Column, DateTime, String, Table
from sqlalchemy.dialects.postgresql import UUID

from src.database.database import default_now, metaData, new_uuid, now

permission_types = Table(
    "permission_types",
    metaData,
    Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False, default=new_uuid
    ),
    Column("name", String, nullable=False),
    Column("symbol", String, nullable=False),
    Column("created_at", DateTime, nullable=False, **default_now),
    Column("updated_at", DateTime, onupdate=now, nullable=False, **default_now),
)
