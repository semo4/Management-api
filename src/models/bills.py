from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID

from src.database.database import default_now, metaData, new_uuid, now

bills = Table(
    "bills",
    metaData,
    Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False, default=new_uuid
    ),
    Column("store_name", String, nullable=False),
    Column("buyer_name", String, nullable=False),
    Column("item", String, nullable=False),
    Column("amount", Float, nullable=False),
    Column("bill_number", Integer, nullable=False),
    Column("bill_picture", String, nullable=False),
    Column(
        "project_id",
        UUID,
        ForeignKey("projects.id", name="fk_project_id_bills", ondelete="cascade"),
        nullable=False,
    ),
    Column("created_at", DateTime, nullable=False, **default_now),
    Column("updated_at", DateTime, nullable=False, onupdate=now, **default_now),
)
