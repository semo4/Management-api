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

projects = Table(
    "projects",
    metaData,
    Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False, default=new_uuid
    ),
    Column("name", String, nullable=False),
    Column("place", String, nullable=False),
    Column("description", String, nullable=False),
    Column("start_date", DateTime, nullable=False),
    Column("end_date", DateTime, nullable=False),
    Column(
        "section_id",
        UUID,
        ForeignKey("sections.id", name="fk_section_id_projects", ondelete="cascade"),
        nullable=False,
    ),
    Column("project_evaluation", Float, nullable=False),
    Column("created_at", DateTime, nullable=False, **default_now),
    Column("updated_at", DateTime, nullable=False, onupdate=now, **default_now),
    UniqueConstraint("name", name="unique_projects_name"),
)
