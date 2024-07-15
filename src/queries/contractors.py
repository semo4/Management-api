from uuid import UUID

from sqlalchemy.sql import select

from src.database.connection import execute_all, execute_one
from src.database.database import ALL_COLUMNS
from src.models.contractors import contractors
from src.models.projects import projects
from src.models.sections import sections
from src.types.contractors import ContractorsRequest
from src.utils.calculation import calculation_contractors


class ContractorsQueries:
    def get_contractors(self):
        join_table = contractors.join(
            sections, contractors.c.section_id == sections.c.id
        ).join(projects, contractors.c.project_id == projects.c.id)
        res = (
            select(contractors, sections.c.name, projects.c.name)
            .select_from(join_table)
            .where(contractors.c.section_id == sections.c.id)
            .where(contractors.c.project_id == projects.c.id)
        )
        result = execute_all(res)
        return result

    def get_contractor(self, contractor_id: UUID):
        join_table = contractors.join(
            sections, contractors.c.section_id == sections.c.id
        ).join(projects, contractors.c.project_id == projects.c.id)
        result = (
            select(contractors, sections.c.name, projects.c.name)
            .select_from(join_table)
            .where(contractors.c.section_id == sections.c.id)
            .where(contractors.c.project_id == projects.c.id)
            .where(contractors.c.id == contractor_id)
        )
        row = execute_one(result)
        return row

    def get_contractor_by_name(self, contractor_name: str):
        join_table = contractors.join(
            sections, contractors.c.section_id == sections.c.id
        ).join(projects, contractors.c.project_id == projects.c.id)
        result = (
            select(contractors, sections.c.name, projects.c.name)
            .select_from(join_table)
            .where(contractors.c.section_id == sections.c.id)
            .where(contractors.c.project_id == projects.c.id)
            .where(contractors.c.name == contractor_name)
        )
        row = execute_one(result)
        return row

    def insert_contractor(self, contractors_req: ContractorsRequest):
        calculated_data = calculation_contractors(dict(contractors_req))
        result = contractors.insert().values(calculated_data).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row

    def get_contractor_by_id(contractor_id: UUID):
        result = contractors.select().where(contractors.c.id == contractor_id)
        row = execute_one(result)
        return row

    def delete_contractor(self, contractor_id: UUID):
        result = (
            contractors.delete()
            .where(contractors.c.id == contractor_id)
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_contractor(contractor_id: UUID, contractors_req: ContractorsRequest):
        calculated_data = calculation_contractors(
            dict(contractors_req.dict(exclude_unset=True))
        )
        result = (
            contractors.update()
            .where(contractors.c.id == contractor_id)
            .values(calculated_data)
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row
