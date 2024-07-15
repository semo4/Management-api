from uuid import UUID

from src.database.connection import execute_all, execute_one
from src.database.database import ALL_COLUMNS
from src.models.workers import workers
from src.types.workers import WorkersRequest


class WorkersQueries:
    def get_workers(self):
        result = execute_all(workers.select())
        return result

    def get_worker(self, worker_id: UUID):
        result = workers.select().where(workers.c.id == worker_id)
        row = execute_one(result)
        return row

    def get_worker_by_name(self, worker_name: str):
        result = workers.select().where(workers.c.name == worker_name)
        row = execute_one(result)
        return row

    def insert_worker(self, workers_req: WorkersRequest):
        result = workers.insert().values(dict(workers_req)).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row

    def get_worker_by_id(self, worker_id: UUID):
        result = workers.select().where(workers.c.id == worker_id)
        row = execute_one(result)
        return row

    def delete_worker(self, worker_id: UUID):
        result = (
            workers.delete().where(workers.c.id == worker_id).returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_worker(self, worker_id: UUID, workers_req: WorkersRequest):
        result = (
            workers.update()
            .where(workers.c.id == worker_id)
            .values(dict(workers_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row
