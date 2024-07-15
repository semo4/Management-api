from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID

from src.database.database import default_now, metaData, new_uuid, now

contractors = Table(
    "contractors",
    metaData,
    Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False, default=new_uuid
    ),
    Column("name", String, nullable=False),
    Column(
        "project_id",
        UUID,
        ForeignKey("projects.id", name="fk_project_id_contractors"),
        nullable=False,
    ),
    Column(
        "section_id",
        UUID,
        ForeignKey("sections.id", name="fk_section_id_contractors", ondelete="cascade"),
        nullable=False,
    ),
    Column("amount", Float, nullable=False),
    Column("paid_amount", Float, nullable=False),
    Column("rest_amount", Float, nullable=False),
    Column("created_at", DateTime, nullable=False, **default_now),
    Column("updated_at", DateTime, nullable=False, onupdate=now, **default_now),
    UniqueConstraint("name", name="unique_contractors_values"),
)
