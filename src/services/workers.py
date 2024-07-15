from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from src.queries.workers import WorkersQueries
from src.types.workers import WorkersRequest, WorkersResponse
from src.utils.helper import build_workers_dict, build_workers_post_dict

workers_queries = WorkersQueries()


class WorkersServices:
    def get_workers(self) -> jsonable_encoder:
        workers_list = list()
        result = workers_queries.get_workers()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No workers Details Found"
            )
        for row in result:
            data = build_workers_dict(row)
            workers_list.append(data)
        content = jsonable_encoder(WorkersResponse(**dict(i)) for i in workers_list)
        return content

    def get_worker(self, worker_id: UUID) -> jsonable_encoder:
        row = workers_queries.get_worker(worker_id=worker_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No workers Details Found with this ID: {worker_id}",
            )
        data = build_workers_dict(row)
        content = jsonable_encoder(WorkersResponse(**dict(data)))
        return content

    def get_worker_by_name(
        self,
        worker_name: str,
    ) -> jsonable_encoder:
        row = workers_queries.get_worker_by_name(worker_name=worker_name)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No workers Details Found with this Name: {worker_name}",
            )
        data = build_workers_dict(row)
        content = jsonable_encoder(WorkersResponse(**dict(data)))
        return content

    def insert_worker(self, workers_req: WorkersRequest) -> jsonable_encoder:
        row = workers_queries.insert_worker(workers_req=workers_req)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="workers Details Inserted failed",
            )
        data = build_workers_post_dict(row)
        content = jsonable_encoder(WorkersResponse(**dict(data)))
        return content

    def delete_worker(self, worker_id: UUID) -> jsonable_encoder:
        pre_row = workers_queries.get_worker_by_id(worker_id=worker_id)
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No workers Details Found with this ID: {worker_id}",
            )
        else:
            row = workers_queries.delete_worker(worker_id=worker_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"workers Deleted Failed with this ID: {worker_id}",
                )
            data = build_workers_post_dict(row)
            content = jsonable_encoder(WorkersResponse(**dict(data)))
            return content

    def update_worker(
        self, worker_id: UUID, workers_req: WorkersRequest
    ) -> jsonable_encoder:
        row = workers_queries.get_worker_by_id(worker_id=worker_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No workers Details Found with this ID: {worker_id}",
            )
        else:
            row = workers_queries.delete_worker(worker_id=worker_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"workers Deleted Failed with this ID: {worker_id}",
                )
            else:
                row = workers_queries.insert_worker(workers_req=workers_req)
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="workers Details Updated failed",
                    )
                data = build_workers_post_dict(row)
                content = jsonable_encoder(WorkersResponse(**dict(data)))
                return content

    def update(self, worker_id: UUID, workers_req: WorkersRequest) -> jsonable_encoder:
        row = workers_queries.get_worker_by_id(worker_id=worker_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No workers Details Found with this ID: {worker_id}",
            )
        else:
            row = workers_queries.update_worker(
                worker_id=worker_id, workers_req=workers_req
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="workers Details Updated failed",
                )
            data = build_workers_post_dict(row)
            content = jsonable_encoder(WorkersResponse(**dict(data)))
            return content
