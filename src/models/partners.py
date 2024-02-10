from sqlalchemy import Table, Column, String, Float, DateTime, ForeignKey
from src.database.database import metaData, now, default_now, new_uuid
from sqlalchemy.dialects.postgresql import UUID


partners = Table(
    "partners",
    metaData,
    Column('id', UUID(as_uuid=True), primary_key=True,
           nullable=False, default=new_uuid),
    Column('name', String, nullable=False),
    Column('amount', Float, nullable=False),
    Column('pre_amount', Float, nullable=False),
    Column('section_id', UUID, ForeignKey('sections.id',
           name='fk_section_id_partners', ondelete='cascade'), nullable=False),
    Column('created_at', DateTime, nullable=False, **default_now),
    Column('updated_at', DateTime, nullable=False, onupdate=now,
           **default_now)
)
