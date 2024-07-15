from uuid import UUID

from fastapi import APIRouter
from sqlalchemy.sql import select

from src.database.connection import execute_all, execute_one
from src.database.database import ALL_COLUMNS
from src.models.partners import partners
from src.models.sections import sections
from src.types.partners import PartnersRequest

partners_router = APIRouter(prefix="/partners", tags=["Partners"])


class PartnersQueries:
    def get_partners(self):
        join_table = partners.join(sections, partners.c.section_id == sections.c.id)
        res = (
            select(partners, sections.c.name)
            .select_from(join_table)
            .where(partners.c.section_id == sections.c.id)
        )
        result = execute_all(res)
        return result

    def get_partner(self, partner_id: UUID):
        join_table = partners.join(sections, partners.c.section_id == sections.c.id)
        result = (
            select(partners, sections.c.name)
            .select_from(join_table)
            .where(partners.c.section_id == sections.c.id)
            .where(partners.c.id == partner_id)
        )
        row = execute_one(result)
        return row

    def get_partner_by_name(self, partner_name: str):
        result = (
            select(partners, sections.c.name)
            .select_from(
                partners.join(sections, partners.c.section_id == sections.c.id)
            )
            .where(partners.c.section_id == sections.c.id)
            .where(partners.c.name == partner_name)
        )
        row = execute_one(result)
        return row

    def insert_partner(self, partners_req: PartnersRequest):
        result = partners.insert().values(dict(partners_req)).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row

    def get_partner_by_id(self, partner_id: UUID):
        result = partners.select().where(partners.c.id == partner_id)
        row = execute_one(result)
        return row

    def delete_partner(self, partner_id: UUID):
        result = (
            partners.delete().where(partners.c.id == partner_id).returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_partner(self, partner_id: UUID, partners_req: PartnersRequest):
        result = (
            partners.update()
            .where(partners.c.id == partner_id)
            .values(dict(partners_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row
