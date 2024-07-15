from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID

from src.database.database import default_now, metaData, new_uuid, now

outcomes = Table(
    "outcomes",
    metaData,
    Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False, default=new_uuid
    ),
    Column("buyer_name", String, primary_key=True, nullable=False),
    Column("amount_payed", Float, nullable=False),
    Column(
        "project_id",
        String,
        ForeignKey("projects.id", name="fk_project_name_outcomes", ondelete="cascade"),
        nullable=False,
    ),
    Column(
        "category_id",
        String,
        ForeignKey("categories.id", name="fk_category_id_outcomes", ondelete="cascade"),
        nullable=False,
    ),
    Column("reason", String, nullable=False),
    Column("date", DateTime, nullable=False),
    Column("created_at", DateTime, nullable=False, **default_now),
    Column("updated_at", DateTime, nullable=False, onupdate=now, **default_now),
)
