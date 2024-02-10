from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.database.database import ALL_COLUMNS
from uuid import UUID
from src.models.salaries import salaries
from src.models.projects import projects
from src.models.sections import sections
from src.models.workers import workers
from src.types.salaries import SalariesRequest, SalariesResponse
from src.database.connection import execute_all, execute_one
from src.utils.helper import build_salaries_dict, build_salaries_dict_post
from sqlalchemy.sql import select
from src.auth.oauth2 import get_current_user
from src.types.users import Login


salaries_router = APIRouter(prefix='/salaries', tags=['Salaries'])


@salaries_router.get('/', response_model=SalariesResponse)
async def get_salaries(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    salaries_list = list()
    join_table = salaries.join(
        sections, salaries.c.section_id == sections.c.id).join(projects, salaries.c.project_id == projects.c.id).join(workers, salaries.c.worker_id == workers.c.id)
    res = select(salaries, projects.c.name, workers.c.name, sections.c.name).select_from(
        join_table).where(salaries.c.section_id == sections.c.id).where(salaries.c.project_id == projects.c.id).where(salaries.c.worker_id == workers.c.id)
    result = execute_all(res)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No salaries Details Found')
    for row in result:
        data = build_salaries_dict(row)
        salaries_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(SalariesResponse(**dict(i)) for i in salaries_list))


@salaries_router.get('/get_salary/{salaries_id}', response_model=SalariesResponse)
async def get_salary(salaries_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = salaries.join(
        sections, salaries.c.section_id == sections.c.id).join(projects, salaries.c.project_id == projects.c.id).join(workers, salaries.c.worker_id == workers.c.id)
    result = select(salaries, projects.c.name, workers.c.name, sections.c.name).select_from(
        join_table).where(salaries.c.section_id == sections.c.id).where(salaries.c.project_id == projects.c.id).where(salaries.c.worker_id == workers.c.id).where(salaries.c.id == salaries_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No salaries Details Found with this ID: {salaries_id}')
    data = build_salaries_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(SalariesResponse(**dict(data))))


@salaries_router.get('/get_salary_by_salary_type/{salary_type}', response_model=SalariesResponse)
async def get_salary_by_salary_type(salary_type: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = salaries.join(
        sections, salaries.c.section_id == sections.c.id).join(
        projects, salaries.c.project_id == projects.c.id).join(
        workers, salaries.c.worker_id == workers.c.id)
    result = select(salaries, projects.c.name, workers.c.name, sections.c.name).select_from(
        join_table).where(salaries.c.section_id == sections.c.id).where(
            salaries.c.project_id == projects.c.id).where(
            salaries.c.worker_id == workers.c.id).where(
            salaries.c.salary_type == salary_type)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No salaries Details Found with this ID: {salary_type}')
    data = build_salaries_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(SalariesResponse(**dict(data))))


@salaries_router.post('/', response_model=SalariesResponse)
async def insert_salary(salaries_req: SalariesRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = salaries.insert().values(dict(salaries_req)).returning(ALL_COLUMNS)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='salaries Details Inserted failed')
    data = build_salaries_dict_post(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(SalariesResponse(**dict(data))))


@salaries_router.delete('/{salaries_id}', response_model=SalariesResponse)
async def delete_salary(salaries_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = salaries.select().where(salaries.c.id == salaries_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No salaries Details Found with this ID: {salaries_id}')
    else:
        result = salaries.delete().where(
            salaries.c.id == salaries_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'salaries Deleted Failed with this ID: {salaries_id}')
        data = build_salaries_dict_post(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(SalariesResponse(**dict(data))))


@salaries_router.put('/{salaries_id}', response_model=SalariesResponse)
async def update_salary(salaries_id: UUID, salaries_req: SalariesRequest, current_user: Login = Depends(get_current_user)):
    result = salaries.select().where(salaries.c.id == salaries_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No salaries Details Found with this ID: {salaries_id}')
    else:
        result = salaries.delete().where(
            salaries.c.id == salaries_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'salaries Deleted Failed with this ID: {salaries_id}')
        else:
            result = salaries.insert().values(dict(salaries_req)).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='salaries Details Updated failed')
            data = build_salaries_dict_post(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(SalariesResponse(**dict(data))))


@salaries_router.patch('/{salaries_id}', response_model=SalariesResponse)
async def update(salaries_id: UUID, salaries_req: SalariesRequest, current_user: Login = Depends(get_current_user)):
    result = salaries.select().where(salaries.c.id == salaries_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No salaries Details Found with this ID: {salaries_id}')
    else:
        result = salaries.update().where(salaries.c.id == salaries_id).values(
            dict(salaries_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='salaries Details Updated failed')
        data = build_salaries_dict_post(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(SalariesResponse(**dict(data))))
