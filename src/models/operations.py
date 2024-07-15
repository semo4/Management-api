from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID

from src.database.database import default_now, metaData, new_uuid, now

operations = Table(
    "operations",
    metaData,
    Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False, default=new_uuid
    ),
    Column(
        "section_id",
        UUID,
        ForeignKey("sections.id", name="fk_section_id_operations", ondelete="cascade"),
        nullable=False,
    ),
    Column(
        "project_id",
        UUID,
        ForeignKey("projects.id", name="fk_project_id_operations", ondelete="cascade"),
        nullable=False,
    ),
    Column(
        "worker_id",
        UUID,
        ForeignKey("workers.id", name="fk_worker_id_operations", ondelete="cascade"),
        nullable=False,
    ),
    Column(
        "work_place_id",
        UUID,
        ForeignKey(
            "workplace.id", name="fk_work_place_id_operations", ondelete="cascade"
        ),
        nullable=False,
    ),
    Column("working_hours", Integer, nullable=False),
    Column("payment_amount", Float, nullable=False),
    Column("description", String, nullable=False),
    Column("operation_add_date", DateTime, nullable=False, **default_now),
    Column("created_at", DateTime, nullable=False, **default_now),
    Column("updated_at", DateTime, nullable=False, onupdate=now, **default_now),
)
