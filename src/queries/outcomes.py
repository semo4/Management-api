from datetime import datetime
from uuid import UUID

from fastapi import APIRouter
from sqlalchemy.sql import select

from src.database.connection import execute_all, execute_one
from src.database.database import ALL_COLUMNS
from src.models.outcomes import outcomes
from src.models.outcomes_categories import categories
from src.models.projects import projects
from src.types.outcomes import OutcomesRequest

outcomes_router = APIRouter(prefix="/outcomes", tags=["Outcomes"])


class OutcomesQueries:
    def get_outcomes(self):
        join_table = outcomes.join(
            categories, outcomes.c.category_id == categories.c.id
        ).join(projects, outcomes.c.project_id == projects.c.id)
        res = (
            select(outcomes, categories.c.title, projects.c.name)
            .select_from(join_table)
            .where(outcomes.c.category_id == categories.c.id)
            .where(outcomes.c.project_id == projects.c.id)
        )
        result = execute_all(res)
        return result

    def get_outcome(self, outcome_id: UUID):
        join_table = outcomes.join(
            categories, outcomes.c.category_id == categories.c.id
        ).join(projects, outcomes.c.project_id == projects.c.id)
        result = (
            select(outcomes, categories.c.title, projects.c.name)
            .select_from(join_table)
            .where(outcomes.c.category_id == categories.c.id)
            .where(outcomes.c.project_id == projects.c.id)
            .where(outcomes.c.id == outcome_id)
        )
        row = execute_one(result)
        return row

    def get_outcome_by_buyer_name(self, outcome_buyer_name: str):
        join_table = outcomes.join(
            categories, outcomes.c.category_id == categories.c.id
        ).join(projects, outcomes.c.project_id == projects.c.id)
        result = (
            select(outcomes, categories.c.title, projects.c.name)
            .select_from(join_table)
            .where(outcomes.c.category_id == categories.c.id)
            .where(outcomes.c.project_id == projects.c.id)
            .where(outcomes.c.buyer_name == outcome_buyer_name)
        )
        row = execute_one(result)
        return row

    def get_outcome_by_amount_payed(self, outcome_amount_payed: float):
        join_table = outcomes.join(
            categories, outcomes.c.category_id == categories.c.id
        ).join(projects, outcomes.c.project_id == projects.c.id)
        result = (
            select(outcomes, categories.c.title, projects.c.name)
            .select_from(join_table)
            .where(outcomes.c.category_id == categories.c.id)
            .where(outcomes.c.project_id == projects.c.id)
            .where(outcomes.c.amount_payed == outcome_amount_payed)
        )
        row = execute_one(result)
        return row

    def get_outcome_by_date(self, outcome_date: datetime):
        join_table = outcomes.join(
            categories, outcomes.c.category_id == categories.c.id
        ).join(projects, outcomes.c.project_id == projects.c.id)
        result = (
            select(outcomes, categories.c.title, projects.c.name)
            .select_from(join_table)
            .where(outcomes.c.category_id == categories.c.id)
            .where(outcomes.c.project_id == projects.c.id)
            .where(outcomes.c.date == outcome_date)
        )
        row = execute_one(result)
        return row

    def insert_outcome(self, outcomes_req: OutcomesRequest):
        result = outcomes.insert().values(dict(outcomes_req)).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row

    def get_outcome_by_id(self, outcome_id: UUID):
        result = outcomes.select().where(outcomes.c.id == outcome_id)
        row = execute_one(result)
        return row

    def delete_outcome(self, outcome_id: UUID):
        result = (
            outcomes.delete().where(outcomes.c.id == outcome_id).returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_outcome(self, outcome_id: UUID, outcomes_req: OutcomesRequest):
        result = (
            outcomes.update()
            .where(outcomes.c.id == outcome_id)
            .values(dict(outcomes_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row
