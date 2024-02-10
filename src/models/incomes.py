from sqlalchemy import Table, Column, ForeignKey, String, Float, DateTime, Integer
from src.database.database import metaData, now, default_now, new_uuid
from sqlalchemy.dialects.postgresql import UUID


incomes = Table(
    "incomes",
    metaData,
    Column('id', UUID(as_uuid=True), primary_key=True,
           nullable=False, default=new_uuid),
    Column('project_id', UUID, ForeignKey('projects.id',
           name='fk_project_id_income', ondelete='cascade'), nullable=False),
    Column('section_id', UUID, ForeignKey('sections.id',
           name='fk_section_id_income', ondelete='cascade'), nullable=False),
    Column('receiving_person', String, nullable=False),
    Column('gave_person', String, nullable=False),
    Column('check_number', Integer, nullable=False),
    Column('payment_number', Integer, nullable=False),
    Column('amount', Float, nullable=False),
    Column('way_of_receiving', String, nullable=False),
    Column('description', String, nullable=False),
    Column('receiving_date', DateTime, nullable=False, **default_now),
    Column('created_at', DateTime, nullable=False, **default_now),
    Column('updated_at', DateTime, nullable=False, onupdate=now,
           **default_now)
)
