from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.database.database import ALL_COLUMNS
from uuid import UUID
from src.models.workers import workers
from src.types.workers import WorkersRequest, WorkersResponse
from src.database.connection import execute_all, execute_one
from src.utils.helper import build_workers_dict, build_workers_post_dict
from src.auth.oauth2 import get_current_user
from src.types.users import Login

workers_router = APIRouter(prefix='/workers', tags=['Workers'])


@workers_router.get('/', response_model=WorkersResponse)
async def get_workers(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    workers_list = list()
    result = execute_all(workers.select())
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No workers Details Found')
    for row in result:
        data = build_workers_dict(row)
        workers_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(WorkersResponse(**dict(i)) for i in workers_list))


@workers_router.get('/get_worker/{worker_id}', response_model=WorkersResponse)
async def get_worker(worker_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = workers.select().where(workers.c.id == worker_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No workers Details Found with this ID: {worker_id}')
    data = build_workers_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(WorkersResponse(**dict(data))))


@workers_router.get('/get_worker_by_name/{worker_name}', response_model=WorkersResponse)
async def get_worker_by_name(worker_name: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = workers.select().where(workers.c.name == worker_name)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No workers Details Found with this Name: {worker_name}')
    data = build_workers_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(WorkersResponse(**dict(data))))


@workers_router.post('/', response_model=WorkersResponse)
async def insert_worker(workers_req: WorkersRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = workers.insert().values(dict(workers_req)).returning(ALL_COLUMNS)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='workers Details Inserted failed')
    data = build_workers_post_dict(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(WorkersResponse(**dict(data))))


@workers_router.delete('/{worker_id}', response_model=WorkersResponse)
async def delete_worker(worker_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = workers.select().where(workers.c.id == worker_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No workers Details Found with this ID: {worker_id}')
    else:
        result = workers.delete().where(
            workers.c.id == worker_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'workers Deleted Failed with this ID: {worker_id}')
        data = build_workers_post_dict(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(WorkersResponse(**dict(data))))


@workers_router.put('/{worker_id}', response_model=WorkersResponse)
async def update_worker(worker_id: UUID, workers_req: WorkersRequest, current_user: Login = Depends(get_current_user)):
    result = workers.select().where(workers.c.id == worker_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No workers Details Found with this ID: {worker_id}')
    else:
        result = workers.delete().where(
            workers.c.id == worker_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'workers Deleted Failed with this ID: {worker_id}')
        else:
            result = workers.insert().values(dict(workers_req)).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='workers Details Updated failed')
            data = build_workers_post_dict(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(WorkersResponse(**dict(data))))


@workers_router.patch('/{worker_id}', response_model=WorkersResponse)
async def update(worker_id: UUID, workers_req: WorkersRequest, current_user: Login = Depends(get_current_user)):
    result = workers.select().where(workers.c.id == worker_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No workers Details Found with this ID: {worker_id}')
    else:
        result = workers.update().where(workers.c.id == worker_id).values(
            dict(workers_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='workers Details Updated failed')
        data = build_workers_post_dict(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(WorkersResponse(**dict(data))))
