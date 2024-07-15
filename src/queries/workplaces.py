from uuid import UUID

from src.database.connection import execute_all, execute_one
from src.database.database import ALL_COLUMNS
from src.models.workplaces import workplace
from src.types.workplaces import WorkPlacesRequest


class WorkPlaceQueries:
    def get_workplaces(self):
        result = execute_all(workplace.select())
        return result

    def get_workplace(self, workplace_id: UUID):
        result = workplace.select().where(workplace.c.id == workplace_id)
        row = execute_one(result)
        return row

    def get_workplace_by_title(self, workplace_title: str):
        result = workplace.select().where(workplace.c.title == workplace_title)
        row = execute_one(result)
        return row

    def insert_workplace(self, workplace_req: WorkPlacesRequest):
        result = workplace.insert().values(dict(workplace_req)).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row

    def get_workplace_by_id(self, workplace_id: UUID):
        result = workplace.select().where(workplace.c.id == workplace_id)
        row = execute_one(result)
        return row

    def delete_workplace(self, workplace_id: UUID):
        result = (
            workplace.delete()
            .where(workplace.c.id == workplace_id)
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_workplace(
        self,
        workplace_id: UUID,
        workplace_req: WorkPlacesRequest,
    ):
        result = (
            workplace.update()
            .where(workplace.c.id == workplace_id)
            .values(dict(workplace_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row
