from uuid import UUID

from sqlalchemy.sql import select

from src.database.connection import execute_all, execute_one
from src.database.database import ALL_COLUMNS
from src.models.incomes import incomes
from src.models.projects import projects
from src.models.sections import sections
from src.types.incomes import IncomesRequest


class IncomesQueries:
    def get_incomes(self):
        join_table = incomes.join(sections, incomes.c.section_id == sections.c.id).join(
            projects, incomes.c.project_id == projects.c.id
        )
        res = (
            select(incomes, sections.c.name, projects.c.name)
            .select_from(join_table)
            .where(incomes.c.section_id == sections.c.id)
            .where(incomes.c.project_id == projects.c.id)
        )
        result = execute_all(res)
        return result

    def get_income(self, income_id: UUID):
        join_table = incomes.join(sections, incomes.c.section_id == sections.c.id).join(
            projects, incomes.c.project_id == projects.c.id
        )
        result = (
            select(incomes, sections.c.name, projects.c.name)
            .select_from(join_table)
            .where(incomes.c.section_id == sections.c.id)
            .where(incomes.c.project_id == projects.c.id)
            .where(incomes.c.id == income_id)
        )
        row = execute_one(result)
        return row

    def get_income_by_receiving_person(self, income_receiving_person: str):
        join_table = incomes.join(sections, incomes.c.section_id == sections.c.id).join(
            projects, incomes.c.project_id == projects.c.id
        )
        result = (
            select(incomes, sections.c.name, projects.c.name)
            .select_from(join_table)
            .where(incomes.c.section_id == sections.c.id)
            .where(incomes.c.project_id == projects.c.id)
            .where(incomes.c.receiving_person == income_receiving_person)
        )
        row = execute_one(result)
        return row

    def get_income_by_gave_person(self, income_gave_person: str):
        join_table = incomes.join(sections, incomes.c.section_id == sections.c.id).join(
            projects, incomes.c.project_id == projects.c.id
        )
        result = (
            select(incomes, sections.c.name, projects.c.name)
            .select_from(join_table)
            .where(incomes.c.section_id == sections.c.id)
            .where(incomes.c.project_id == projects.c.id)
            .where(incomes.c.gave_person == income_gave_person)
        )
        row = execute_one(result)
        return row

    def get_income_by_check_number(self, income_check_number: int):
        join_table = incomes.join(sections, incomes.c.section_id == sections.c.id).join(
            projects, incomes.c.project_id == projects.c.id
        )
        result = (
            select(incomes, sections.c.name, projects.c.name)
            .select_from(join_table)
            .where(incomes.c.section_id == sections.c.id)
            .where(incomes.c.project_id == projects.c.id)
            .where(incomes.c.check_number == income_check_number)
        )
        row = execute_one(result)
        return row

    def get_income_by_way_of_receiving(self, income_way_of_receiving: str):
        join_table = incomes.join(sections, incomes.c.section_id == sections.c.id).join(
            projects, incomes.c.project_id == projects.c.id
        )
        result = (
            select(incomes, sections.c.name, projects.c.name)
            .select_from(join_table)
            .where(incomes.c.section_id == sections.c.id)
            .where(incomes.c.project_id == projects.c.id)
            .where(incomes.c.way_of_receiving == income_way_of_receiving)
        )
        row = execute_one(result)
        return row

    def insert_income(self, incomes_req: IncomesRequest):
        result = incomes.insert().values(dict(incomes_req)).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row

    def get_income_by_id(self, income_id: UUID):
        result = incomes.select().where(incomes.c.id == income_id)
        row = execute_one(result)
        return row

    def delete_income(self, income_id: UUID):
        result = (
            incomes.delete().where(incomes.c.id == income_id).returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_income(self, income_id: UUID, incomes_req: IncomesRequest):
        result = (
            incomes.update()
            .where(incomes.c.id == income_id)
            .values(dict(incomes_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row
