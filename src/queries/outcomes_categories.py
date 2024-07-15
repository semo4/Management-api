from uuid import UUID

from fastapi import APIRouter

from src.database.connection import execute_all, execute_one
from src.database.database import ALL_COLUMNS
from src.models.outcomes_categories import categories
from src.types.outcomes_categories import OutcomesCategoriesRequest

categories_router = APIRouter(prefix="/categories", tags=["Categories"])


class OutcomesCategoriesQueries:
    def get_categories(self):
        result = execute_all(categories.select())
        return result

    def get_category(self, categories_id: UUID):
        result = categories.select().where(categories.c.id == categories_id)
        row = execute_one(result)
        return row

    def get_categories_by_title(self, categories_title: str):
        result = categories.select().where(categories.c.title == categories_title)
        row = execute_one(result)
        return row

    def insert_categories(self, categories_req: OutcomesCategoriesRequest):
        result = categories.insert().values(dict(categories_req)).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row

    def delete_categories(self, categories_id: UUID):
        result = (
            categories.delete()
            .where(categories.c.id == categories_id)
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_categories(
        self, categories_id: UUID, categories_req: OutcomesCategoriesRequest
    ):
        result = (
            categories.update()
            .where(categories.c.id == categories_id)
            .values(dict(categories_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row
