from sqlalchemy import Table, Column, String, Float, DateTime, ForeignKey
from src.database.database import metaData, now, default_now, new_uuid
from sqlalchemy.dialects.postgresql import UUID


salaries = Table(
    "salaries",
    metaData,
    Column('id', UUID(as_uuid=True), primary_key=True,
           nullable=False, default=new_uuid),
    Column('project_id', UUID, ForeignKey('projects.id',
           name='fk_project_id_salaries', ondelete='cascade'), nullable=False),
    Column('worker_id', UUID, ForeignKey('workers.id',
           name='fk_worker_id_salaries', ondelete='cascade'), nullable=False),
    Column('section_id', UUID, ForeignKey('sections.id',
           name='fk_section_id_salaries', ondelete='cascade'), nullable=False),
    Column('salary_type', String, nullable=False),
    Column('amount', Float, nullable=False),
    Column('date', DateTime, nullable=False),
    Column('created_at', DateTime, nullable=False, **default_now),
    Column('updated_at', DateTime, nullable=False, onupdate=now,
           **default_now)
)
