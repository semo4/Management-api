from typing import Literal
from uuid import UUID

from sqlalchemy.engine import Row
from sqlalchemy.schema import Sequence
from sqlalchemy.sql import select

from src.database.connection import execute_all, execute_one
from src.database.database import ALL_COLUMNS
from src.models.bills import bills
from src.models.projects import projects
from src.types.bills import BillsRequest


class BillsQueries:
    def get_bills(self) -> Sequence[Row] | Literal[False]:
        join_table = bills.join(projects, bills.c.project_id == projects.c.id)
        res = (
            select(bills, projects.c.name)
            .select_from(join_table)
            .where(bills.c.project_id == projects.c.id)
        )
        result = execute_all(res)
        return result

    def get_bill(self, bill_id: UUID) -> Row | Literal[False]:
        join_table = bills.join(projects, bills.c.project_id == projects.c.id)
        result = (
            select(bills, projects.c.name)
            .select_from(join_table)
            .where(bills.c.project_id == projects.c.id)
            .where(bills.c.id == bill_id)
        )
        row = execute_one(result)
        return row

    def get_bill_by_name(self, bill_store_name: str) -> Row | Literal[False]:
        result = (
            select(bills, projects.c.name)
            .select_from(bills.join(projects, bills.c.project_id == projects.c.id))
            .where(bills.c.project_id == projects.c.id)
            .where(bills.c.store_name == bill_store_name)
        )
        row = execute_one(result)
        return row

    def get_bill_by_buyer_name(self, bill_buyer_name: str) -> Row | Literal[False]:
        result = (
            select(bills, projects.c.name)
            .select_from(bills.join(projects, bills.c.project_id == projects.c.id))
            .where(bills.c.project_id == projects.c.id)
            .where(bills.c.buyer_name == bill_buyer_name)
        )
        row = execute_one(result)
        return row

    def get_bill_by_bill_number(self, bill_number: int) -> Row | Literal[False]:
        result = (
            select(bills, projects.c.name)
            .select_from(bills.join(projects, bills.c.project_id == projects.c.id))
            .where(bills.c.project_id == projects.c.id)
            .where(bills.c.bill_number == bill_number)
        )
        row = execute_one(result)
        return row

    def insert_bill(self, bills_req: BillsRequest) -> Row | Literal[False]:
        result = bills.insert().values(dict(bills_req)).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row

    def get_bill_by_id(self, bill_id: UUID) -> Row | Literal[False]:
        result = bills.select().where(bills.c.id == bill_id)
        row = execute_one(result)
        return row

    def delete_bill(self, bill_id: UUID) -> Row | Literal[False]:
        result = bills.delete().where(bills.c.id == bill_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row

    def update_bill(
        self, bill_id: UUID, bills_req: BillsRequest
    ) -> Row | Literal[False]:
        result = (
            bills.update()
            .where(bills.c.id == bill_id)
            .values(dict(bills_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row
