from uuid import UUID

from sqlalchemy.sql import select

from src.database.connection import execute_all, execute_one
from src.database.database import ALL_COLUMNS
from src.models.partners import partners
from src.models.projects import projects
from src.models.sections import sections
from src.models.withdraw import withdraw
from src.types.withdraw import WithdrawRequest


class WithdrawQueries:
    def get_withdraws(self):
        join_table = (
            withdraw.join(sections, withdraw.c.section_id == sections.c.id)
            .join(projects, withdraw.c.project_id == projects.c.id)
            .join(partners, withdraw.c.partner_id == partners.c.id)
        )
        res = (
            select(withdraw, sections.c.name, projects.c.name, partners.c.name)
            .select_from(join_table)
            .where(withdraw.c.section_id == sections.c.id)
            .where(withdraw.c.project_id == projects.c.id)
            .where(withdraw.c.partner_id == partners.c.id)
        )
        result = execute_all(res)
        return result

    def get_withdraw(self, withdraw_id: UUID):
        join_table = (
            withdraw.join(sections, withdraw.c.section_id == sections.c.id)
            .join(projects, withdraw.c.project_id == projects.c.id)
            .join(partners, withdraw.c.partner_id == partners.c.id)
        )
        result = (
            select(withdraw, sections.c.name, projects.c.name, partners.c.name)
            .select_from(join_table)
            .where(withdraw.c.section_id == sections.c.id)
            .where(withdraw.c.project_id == projects.c.id)
            .where(withdraw.c.partner_id == partners.c.id)
            .where(withdraw.c.id == withdraw_id)
        )
        row = execute_one(result)
        return row

    def get_withdraw_by_amount(self, withdraw_amount: float):
        join_table = (
            withdraw.join(sections, withdraw.c.section_id == sections.c.id)
            .join(projects, withdraw.c.project_id == projects.c.id)
            .join(partners, withdraw.c.partner_id == partners.c.id)
        )
        result = (
            select(withdraw, sections.c.name, projects.c.name, partners.c.name)
            .select_from(join_table)
            .where(withdraw.c.section_id == sections.c.id)
            .where(withdraw.c.project_id == projects.c.id)
            .where(withdraw.c.partner_id == partners.c.id)
            .where(withdraw.c.amount == withdraw_amount)
        )
        row = execute_one(result)
        return row

    def insert_withdraw(self, withdraw_req: WithdrawRequest):
        result = withdraw.insert().values(dict(withdraw_req)).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row

    def get_withdraw_by_id(self, withdraw_id: UUID):
        result = withdraw.select().where(withdraw.c.id == withdraw_id)
        row = execute_one(result)
        return row

    def delete_withdraw(self, withdraw_id: UUID):
        result = (
            withdraw.delete().where(withdraw.c.id == withdraw_id).returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_withdraw(
        self,
        withdraw_id: UUID,
        withdraw_req: WithdrawRequest,
    ):
        result = (
            withdraw.update()
            .where(withdraw.c.id == withdraw_id)
            .values(dict(withdraw_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row
