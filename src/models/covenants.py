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

covenants_cash = Table(
    "covenants_cash",
    metaData,
    Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False, default=new_uuid
    ),
    Column("name", String, nullable=False),
    Column(
        "partner_id",
        UUID,
        ForeignKey("partners.id", name="fk_partner_covenants_cash", ondelete="cascade"),
        nullable=False,
    ),
    Column("price", Float, nullable=False),
    Column("date", DateTime, nullable=False, **default_now),
    Column("created_at", DateTime, nullable=False, **default_now),
    Column("updated_at", DateTime, nullable=False, onupdate=now, **default_now),
    UniqueConstraint("name", name="unique_covenants_cash_values"),
)

covenants_devices = Table(
    "covenants_devices",
    metaData,
    Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False, default=new_uuid
    ),
    Column("title", String, nullable=False),
    Column(
        "worker_id",
        UUID,
        ForeignKey("workers.id", name="fk_workers_covenants_cash", ondelete="cascade"),
        nullable=False,
    ),
    Column("desc", String, nullable=False),
    Column("date", DateTime, nullable=False, **default_now),
    Column("created_at", DateTime, nullable=False, **default_now),
    Column("updated_at", DateTime, nullable=False, onupdate=now, **default_now),
    UniqueConstraint("title", name="unique_covenants_devices_values"),
)
