from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID

from src.database.database import default_now, metaData, new_uuid, now

permissions = Table(
    "permissions",
    metaData,
    Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False, default=new_uuid
    ),
    Column("layer", Integer, nullable=False),
    Column("supervise", String, nullable=True),
    Column("approval", Boolean, nullable=True),
    Column("approval_timestamp", DateTime, nullable=True),
    Column("system_access", JSON, nullable=False),
    Column(
        "project_id",
        UUID,
        ForeignKey("projects.id", name="fk_project_id_permissions", ondelete="cascade"),
        nullable=False,
    ),
    Column(
        "user_id",
        UUID,
        ForeignKey("users.id", name="fk_users_id_permissions", ondelete="cascade"),
        nullable=False,
    ),
    Column("created_at", DateTime, nullable=False, **default_now),
    Column("updated_at", DateTime, nullable=False, onupdate=now, **default_now),
)
