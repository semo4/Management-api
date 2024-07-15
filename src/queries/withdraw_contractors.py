from uuid import UUID

from sqlalchemy.sql import select

from src.database.connection import execute_all, execute_one
from src.database.database import ALL_COLUMNS
from src.models.contractors import contractors
from src.models.projects import projects
from src.models.sections import sections
from src.models.withdraw_contractors import withdraw_contractors
from src.types.withdraw_contractors import WithdrawContractorsRequest


class WithdrawContractorsQueries:
    def get_withdraw_contractors(self):
        join_table = (
            withdraw_contractors.join(
                sections, withdraw_contractors.c.section_id == sections.c.id
            )
            .join(projects, withdraw_contractors.c.project_id == projects.c.id)
            .join(contractors, withdraw_contractors.c.contractor_id == contractors.c.id)
        )
        res = (
            select(
                withdraw_contractors,
                sections.c.name,
                projects.c.name,
                contractors.c.name,
            )
            .select_from(join_table)
            .where(withdraw_contractors.c.section_id == sections.c.id)
            .where(withdraw_contractors.c.project_id == projects.c.id)
            .where(withdraw_contractors.c.contractor_id == contractors.c.id)
        )
        result = execute_all(res)
        return result

    def get_operation(self, withdraw_contractors_id: UUID):
        join_table = (
            withdraw_contractors.join(
                sections, withdraw_contractors.c.section_id == sections.c.id
            )
            .join(projects, withdraw_contractors.c.project_id == projects.c.id)
            .join(contractors, withdraw_contractors.c.contractor_id == contractors.c.id)
        )
        result = (
            select(
                withdraw_contractors,
                sections.c.name,
                projects.c.name,
                contractors.c.name,
            )
            .select_from(join_table)
            .where(withdraw_contractors.c.section_id == sections.c.id)
            .where(withdraw_contractors.c.project_id == projects.c.id)
            .where(withdraw_contractors.c.contractor_id == contractors.c.id)
            .where(withdraw_contractors.c.id == withdraw_contractors_id)
        )
        row = execute_one(result)
        return row

    def get_operation_by_amount(self, withdraw_contractors_amount: float):
        join_table = (
            withdraw_contractors.join(
                sections, withdraw_contractors.c.section_id == sections.c.id
            )
            .join(projects, withdraw_contractors.c.project_id == projects.c.id)
            .join(contractors, withdraw_contractors.c.contractor_id == contractors.c.id)
        )
        result = (
            select(
                withdraw_contractors,
                sections.c.name,
                projects.c.name,
                contractors.c.name,
            )
            .select_from(join_table)
            .where(withdraw_contractors.c.section_id == sections.c.id)
            .where(withdraw_contractors.c.project_id == projects.c.id)
            .where(withdraw_contractors.c.contractor_id == contractors.c.id)
            .where(withdraw_contractors.c.amount == withdraw_contractors_amount)
        )
        row = execute_one(result)
        return row

    def insert_operation(self, withdraw_contractors_req: WithdrawContractorsRequest):
        result = (
            withdraw_contractors.insert()
            .values(dict(withdraw_contractors_req))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def get_operation_by_id(self, withdraw_contractors_id: UUID):
        result = withdraw_contractors.select().where(
            withdraw_contractors.c.id == withdraw_contractors_id
        )
        row = execute_one(result)
        return row

    def delete_withdraw_contractors(self, withdraw_contractors_id: UUID):
        result = (
            withdraw_contractors.delete()
            .where(withdraw_contractors.c.id == withdraw_contractors_id)
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_withdraw_contractors(
        self,
        withdraw_contractors_id: UUID,
        withdraw_contractors_req: WithdrawContractorsRequest,
    ):
        result = (
            withdraw_contractors.update()
            .where(withdraw_contractors.c.id == withdraw_contractors_id)
            .values(dict(withdraw_contractors_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row
