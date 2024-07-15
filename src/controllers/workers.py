from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.oauth2 import get_current_user
from src.services.workers import WorkersServices
from src.types.users import Login
from src.types.workers import WorkersRequest, WorkersResponse

workers_router = APIRouter(prefix="/workers", tags=["Workers"])

workers_services = WorkersServices()


@workers_router.get("/", response_model=WorkersResponse)
async def get_workers(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    content = workers_services.get_workers()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@workers_router.get("/get_worker/{worker_id}", response_model=WorkersResponse)
async def get_worker(
    worker_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = workers_services.get_worker(worker_id=worker_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@workers_router.get("/get_worker_by_name/{worker_name}", response_model=WorkersResponse)
async def get_worker_by_name(
    worker_name: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = workers_services.get_worker_by_name(worker_name=worker_name)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@workers_router.post("/", response_model=WorkersResponse)
async def insert_worker(
    workers_req: WorkersRequest, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = workers_services.insert_worker(workers_req=workers_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@workers_router.delete("/{worker_id}", response_model=WorkersResponse)
async def delete_worker(
    worker_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = workers_services.delete_worker(worker_id=worker_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@workers_router.put("/{worker_id}", response_model=WorkersResponse)
async def update_worker(
    worker_id: UUID,
    workers_req: WorkersRequest,
    current_user: Login = Depends(get_current_user),
):
    content = workers_services.update_worker(
        worker_id=worker_id, workers_req=workers_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@workers_router.patch("/{worker_id}", response_model=WorkersResponse)
async def update(
    worker_id: UUID,
    workers_req: WorkersRequest,
    current_user: Login = Depends(get_current_user),
):
    content = workers_services.update(worker_id=worker_id, workers_req=workers_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )
