from sqlalchemy import Column, DateTime, Float, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from src.database.database import default_now, metaData, new_uuid, now

withdraw_contractors = Table(
    "withdraw_contractors",
    metaData,
    Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False, default=new_uuid
    ),
    Column(
        "section_id",
        UUID,
        ForeignKey("sections.id", name="fk_section_id_outcomes", ondelete="cascade"),
        nullable=False,
    ),
    Column(
        "project_id",
        UUID,
        ForeignKey("projects.id", name="fk_project_id_outcomes", ondelete="cascade"),
        nullable=False,
    ),
    Column(
        "contractor_id",
        UUID,
        ForeignKey(
            "contractors.id", name="fk_contractors_id_outcomes", ondelete="cascade"
        ),
        nullable=False,
    ),
    Column("amount", Float, nullable=False),
    Column("date", DateTime, nullable=False),
    Column("created_at", DateTime, nullable=False, **default_now),
    Column("updated_at", DateTime, nullable=False, onupdate=now, **default_now),
)
