from sqlalchemy import Table, Column, String, Float, DateTime, ForeignKey
from src.database.database import metaData, now, default_now, new_uuid
from sqlalchemy.dialects.postgresql import UUID


withdraw = Table(
    "withdraw",
    metaData,
    Column('id', UUID(as_uuid=True), primary_key=True,
           nullable=False, default=new_uuid),
    Column('section_id', String, ForeignKey('sections.id',
           name='fk_section_id_outcomes', ondelete='cascade'), nullable=False),
    Column('project_id', String, ForeignKey('projects.id',
           name='fk_project_id_outcomes', ondelete='cascade'), nullable=False),
    Column('partner_id', String, ForeignKey('partners.id',
           name='fk_partner_id_outcomes', ondelete='cascade'), nullable=False),
    Column('amount', Float, nullable=False),
    Column('date', DateTime, nullable=False),
    Column('created_at', DateTime, nullable=False, **default_now),
    Column('updated_at', DateTime, nullable=False, onupdate=now,
           **default_now)
)
