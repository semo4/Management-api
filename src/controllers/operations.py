from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.database.database import ALL_COLUMNS
from uuid import UUID
from src.models.operations import operations
from src.models.projects import projects
from src.models.sections import sections
from src.models.workers import workers
from src.models.workplaces import workplace
from src.types.operations import OperationsRequest, OperationsResponse
from src.database.connection import execute_all, execute_one
from src.utils.helper import build_operations_dict, build_operations_dict_post
from sqlalchemy.sql import select
from src.utils.calculation import calculation_operations
from src.auth.oauth2 import get_current_user
from src.types.users import Login

operations_router = APIRouter(prefix='/operations', tags=['Operations'])


@operations_router.get('/', response_model=OperationsResponse)
async def get_operations(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    operations_list = list()
    join_table = operations.join(
        sections, operations.c.section_id == sections.c.id).join(projects, operations.c.project_id == projects.c.id).join(workers, operations.c.worker_id == workers.c.id).join(workplace, operations.c.work_place_id == workplace.c.id)
    res = select(operations, sections.c.name, projects.c.name, workers.c.name, workplace.c.title).select_from(
        join_table).where(operations.c.section_id == sections.c.id).where(operations.c.project_id == projects.c.id).where(operations.c.worker_id == workers.c.id).where(operations.c.work_place_id == workplace.c.id)
    result = execute_all(res)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No operations Details Found')
    for row in result:
        data = build_operations_dict(row)
        operations_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(OperationsResponse(**dict(i)) for i in operations_list))


@operations_router.get('/get_operation/{operations_id}', response_model=OperationsResponse)
async def get_operation(operations_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = operations.join(
        sections, operations.c.section_id == sections.c.id).join(projects, operations.c.project_id == projects.c.id).join(workers, operations.c.worker_id == workers.c.id).join(workplace, operations.c.work_place_id == workplace.c.id)
    result = select(operations, sections.c.name, projects.c.name, workers.c.name, workplace.c.title).select_from(
        join_table).where(operations.c.section_id == sections.c.id).where(operations.c.project_id == projects.c.id).where(operations.c.worker_id == workers.c.id).where(operations.c.work_place_id == workplace.c.id).where(operations.c.id == operations_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No operations Details Found with this ID: {operations_id}')
    data = build_operations_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(OperationsResponse(**dict(data))))


@operations_router.get('/get_operation_by_working_hours/{operations_working_hours}', response_model=OperationsResponse)
async def get_operation_by_working_hours(operations_working_hours: int, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = operations.join(
        sections, operations.c.section_id == sections.c.id).join(
        projects, operations.c.project_id == projects.c.id).join(
        workers, operations.c.worker_id == workers.c.id).join(
        workplace, operations.c.work_place_id == workplace.c.id)
    result = select(operations, sections.c.name, projects.c.name, workers.c.name, workplace.c.title).select_from(
        join_table).where(operations.c.section_id == sections.c.id).where(
            operations.c.project_id == projects.c.id).where(
            operations.c.worker_id == workers.c.id).where(
            operations.c.work_place_id == workplace.c.id).where(
            operations.c.working_hours == operations_working_hours)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No operations Details Found with this ID: {operations_working_hours}')
    data = build_operations_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(OperationsResponse(**dict(data))))


@operations_router.get('/get_operation_by_payment_amount/{operations_payment_amount}', response_model=OperationsResponse)
async def get_operation_by_payment_amount(operations_payment_amount: float, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = operations.join(
        sections, operations.c.section_id == sections.c.id).join(projects, operations.c.project_id == projects.c.id).join(workers, operations.c.worker_id == workers.c.id).join(workplace, operations.c.work_place_id == workplace.c.id)
    result = select(operations, sections.c.name, projects.c.name, workers.c.name, workplace.c.title).select_from(
        join_table).where(operations.c.section_id == sections.c.id).where(operations.c.project_id == projects.c.id).where(operations.c.worker_id == workers.c.id).where(operations.c.work_place_id == workplace.c.id).where(operations.c.payment_amount == operations_payment_amount)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No operations Details Found with this ID: {operations_payment_amount}')
    data = build_operations_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(OperationsResponse(**dict(data))))


@operations_router.post('/', response_model=OperationsResponse)
async def insert_operation(operations_req: OperationsRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    calculated_data = calculation_operations(dict(operations_req))
    if not calculated_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='operations Details Inserted failed')
    result = operations.insert().values(calculated_data).returning(ALL_COLUMNS)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='operations Details Inserted failed')
    data = build_operations_dict_post(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(OperationsResponse(**dict(data))))


@operations_router.delete('/{operations_id}', response_model=OperationsResponse)
async def delete_operations(operations_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = operations.select().where(operations.c.id == operations_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No operations Details Found with this ID: {operations_id}')
    else:
        result = operations.delete().where(
            operations.c.id == operations_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'operations Deleted Failed with this ID: {operations_id}')
        data = build_operations_dict_post(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(OperationsResponse(**dict(data))))


@operations_router.put('/{operations_id}', response_model=OperationsResponse)
async def update_operations(operations_id: UUID, operations_req: OperationsRequest, current_user: Login = Depends(get_current_user)):
    result = operations.select().where(operations.c.id == operations_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No operations Details Found with this ID: {operations_id}')
    else:
        result = operations.delete().where(
            operations.c.id == operations_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'operations Deleted Failed with this ID: {operations_id}')
        else:
            calculated_data = calculation_operations(dict(operations_req))
            if not calculated_data:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='operations Details Inserted failed')
            result = operations.insert().values(calculated_data).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='operations Details Updated failed')
            data = build_operations_dict_post(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(OperationsResponse(**dict(data))))


@operations_router.patch('/{operations_id}', response_model=OperationsResponse)
async def update(operations_id: UUID, operations_req: OperationsRequest, current_user: Login = Depends(get_current_user)):
    result = operations.select().where(operations.c.id == operations_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No operations Details Found with this ID: {operations_id}')
    else:
        calculated_data = calculation_operations(
            dict(operations_req.dict(exclude_unset=True)))
        if not calculated_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='operations Details Inserted failed')
        result = operations.update().where(operations.c.id == operations_id).values(
            calculated_data).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='operations Details Updated failed')
        data = build_operations_dict_post(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(OperationsResponse(**dict(data))))
