from uuid import UUID

from sqlalchemy.sql import select

from src.database.connection import execute_all, execute_one
from src.database.database import ALL_COLUMNS
from src.models.operations import operations
from src.models.projects import projects
from src.models.sections import sections
from src.models.workers import workers
from src.models.workplaces import workplace


class OperationsQueries:
    def get_operations(self):
        join_table = (
            operations.join(sections, operations.c.section_id == sections.c.id)
            .join(projects, operations.c.project_id == projects.c.id)
            .join(workers, operations.c.worker_id == workers.c.id)
            .join(workplace, operations.c.work_place_id == workplace.c.id)
        )
        res = (
            select(
                operations,
                sections.c.name,
                projects.c.name,
                workers.c.name,
                workplace.c.title,
            )
            .select_from(join_table)
            .where(operations.c.section_id == sections.c.id)
            .where(operations.c.project_id == projects.c.id)
            .where(operations.c.worker_id == workers.c.id)
            .where(operations.c.work_place_id == workplace.c.id)
        )
        result = execute_all(res)
        return result

    def get_operation(self, operations_id: UUID):
        join_table = (
            operations.join(sections, operations.c.section_id == sections.c.id)
            .join(projects, operations.c.project_id == projects.c.id)
            .join(workers, operations.c.worker_id == workers.c.id)
            .join(workplace, operations.c.work_place_id == workplace.c.id)
        )
        result = (
            select(
                operations,
                sections.c.name,
                projects.c.name,
                workers.c.name,
                workplace.c.title,
            )
            .select_from(join_table)
            .where(operations.c.section_id == sections.c.id)
            .where(operations.c.project_id == projects.c.id)
            .where(operations.c.worker_id == workers.c.id)
            .where(operations.c.work_place_id == workplace.c.id)
            .where(operations.c.id == operations_id)
        )
        row = execute_one(result)
        return row

    def get_operation_by_working_hours(self, operations_working_hours: int):
        join_table = (
            operations.join(sections, operations.c.section_id == sections.c.id)
            .join(projects, operations.c.project_id == projects.c.id)
            .join(workers, operations.c.worker_id == workers.c.id)
            .join(workplace, operations.c.work_place_id == workplace.c.id)
        )
        result = (
            select(
                operations,
                sections.c.name,
                projects.c.name,
                workers.c.name,
                workplace.c.title,
            )
            .select_from(join_table)
            .where(operations.c.section_id == sections.c.id)
            .where(operations.c.project_id == projects.c.id)
            .where(operations.c.worker_id == workers.c.id)
            .where(operations.c.work_place_id == workplace.c.id)
            .where(operations.c.working_hours == operations_working_hours)
        )
        row = execute_one(result)
        return row

    def get_operation_by_payment_amount(self, operations_payment_amount: float):
        join_table = (
            operations.join(sections, operations.c.section_id == sections.c.id)
            .join(projects, operations.c.project_id == projects.c.id)
            .join(workers, operations.c.worker_id == workers.c.id)
            .join(workplace, operations.c.work_place_id == workplace.c.id)
        )
        result = (
            select(
                operations,
                sections.c.name,
                projects.c.name,
                workers.c.name,
                workplace.c.title,
            )
            .select_from(join_table)
            .where(operations.c.section_id == sections.c.id)
            .where(operations.c.project_id == projects.c.id)
            .where(operations.c.worker_id == workers.c.id)
            .where(operations.c.work_place_id == workplace.c.id)
            .where(operations.c.payment_amount == operations_payment_amount)
        )
        row = execute_one(result)
        return row

    def insert_operation(self, calculated_data: dict):
        result = operations.insert().values(calculated_data).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row

    def get_operation_by_id(self, operations_id: UUID):
        result = operations.select().where(operations.c.id == operations_id)
        row = execute_one(result)
        return row

    def delete_operations(operations_id: UUID):
        result = (
            operations.delete()
            .where(operations.c.id == operations_id)
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_operations(operations_id: UUID, calculated_data: dict):
        result = (
            operations.update()
            .where(operations.c.id == operations_id)
            .values(calculated_data)
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row
