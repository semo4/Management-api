from uuid import UUID

from sqlalchemy.sql import select

from src.database.connection import execute_all, execute_one
from src.database.database import ALL_COLUMNS
from src.models.projects import projects
from src.models.salaries import salaries
from src.models.sections import sections
from src.models.workers import workers
from src.types.salaries import SalariesRequest


class SalariesQueries:
    def get_salaries(self):
        join_table = (
            salaries.join(sections, salaries.c.section_id == sections.c.id)
            .join(projects, salaries.c.project_id == projects.c.id)
            .join(workers, salaries.c.worker_id == workers.c.id)
        )
        res = (
            select(salaries, projects.c.name, workers.c.name, sections.c.name)
            .select_from(join_table)
            .where(salaries.c.section_id == sections.c.id)
            .where(salaries.c.project_id == projects.c.id)
            .where(salaries.c.worker_id == workers.c.id)
        )
        result = execute_all(res)
        return result

    def get_salary(self, salaries_id: UUID):
        join_table = (
            salaries.join(sections, salaries.c.section_id == sections.c.id)
            .join(projects, salaries.c.project_id == projects.c.id)
            .join(workers, salaries.c.worker_id == workers.c.id)
        )
        result = (
            select(salaries, projects.c.name, workers.c.name, sections.c.name)
            .select_from(join_table)
            .where(salaries.c.section_id == sections.c.id)
            .where(salaries.c.project_id == projects.c.id)
            .where(salaries.c.worker_id == workers.c.id)
            .where(salaries.c.id == salaries_id)
        )
        row = execute_one(result)
        return row

    def get_salary_by_salary_type(self, salary_type: str):
        join_table = (
            salaries.join(sections, salaries.c.section_id == sections.c.id)
            .join(projects, salaries.c.project_id == projects.c.id)
            .join(workers, salaries.c.worker_id == workers.c.id)
        )
        result = (
            select(salaries, projects.c.name, workers.c.name, sections.c.name)
            .select_from(join_table)
            .where(salaries.c.section_id == sections.c.id)
            .where(salaries.c.project_id == projects.c.id)
            .where(salaries.c.worker_id == workers.c.id)
            .where(salaries.c.salary_type == salary_type)
        )
        row = execute_one(result)
        return row

    def insert_salary(self, salaries_req: SalariesRequest):
        result = salaries.insert().values(dict(salaries_req)).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row

    def get_salary_by_id(self, salaries_id: UUID):
        result = salaries.select().where(salaries.c.id == salaries_id)
        row = execute_one(result)
        return row

    def delete_salary(self, salaries_id: UUID):
        result = (
            salaries.delete().where(salaries.c.id == salaries_id).returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_salary(self, salaries_id: UUID, salaries_req: SalariesRequest):
        result = (
            salaries.update()
            .where(salaries.c.id == salaries_id)
            .values(dict(salaries_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row
