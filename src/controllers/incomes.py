from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.database.database import ALL_COLUMNS
from uuid import UUID
from src.models.projects import projects
from src.models.sections import sections
from src.models.incomes import incomes
from src.types.incomes import IncomesRequest, IncomesResponse
from src.database.connection import execute_all, execute_one
from src.utils.helper import build_incomes_dict, build_incomes_dict_post
from sqlalchemy.sql import select
from src.auth.oauth2 import get_current_user
from src.types.users import Login


incomes_router = APIRouter(prefix='/incomes', tags=['Incomes'])


@incomes_router.get('/', response_model=IncomesResponse)
async def get_incomes(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    incomes_list = list()
    join_table = incomes.join(
        sections, incomes.c.section_id == sections.c.id).join(projects, incomes.c.project_id == projects.c.id)
    res = select(incomes, sections.c.name, projects.c.name).select_from(
        join_table).where(incomes.c.section_id == sections.c.id).where(incomes.c.project_id == projects.c.id)
    result = execute_all(res)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No incomes Details Found')
    for row in result:
        data = build_incomes_dict(row)
        incomes_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(IncomesResponse(**dict(i)) for i in incomes_list))


@incomes_router.get('/get_income/{income_id}', response_model=IncomesResponse)
async def get_income(income_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = incomes.join(
        sections, incomes.c.section_id == sections.c.id).join(projects, incomes.c.project_id == projects.c.id)
    result = select(incomes, sections.c.name, projects.c.name).select_from(
        join_table).where(incomes.c.section_id == sections.c.id).where(incomes.c.project_id == projects.c.id).where(incomes.c.id == income_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No incomes Details Found with this ID: {income_id}')
    data = build_incomes_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(IncomesResponse(**dict(data, exclude_none=True))))


@incomes_router.get('/get_income_by_receiving_person/{income_receiving_person}', response_model=IncomesResponse)
async def get_income_by_receiving_person(income_receiving_person: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = incomes.join(
        sections, incomes.c.section_id == sections.c.id).join(projects, incomes.c.project_id == projects.c.id)
    result = select(incomes, sections.c.name, projects.c.name).select_from(
        join_table).where(incomes.c.section_id == sections.c.id).where(incomes.c.project_id == projects.c.id).where(incomes.c.receiving_person == income_receiving_person)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No incomes Details Found with this Name: {income_receiving_person}')
    data = build_incomes_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(IncomesResponse(**dict(data))))


@incomes_router.get('/get_income_by_gave_person/{income_gave_person}', response_model=IncomesResponse)
async def get_income_by_gave_person(income_gave_person: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = incomes.join(
        sections, incomes.c.section_id == sections.c.id).join(projects, incomes.c.project_id == projects.c.id)
    result = select(incomes, sections.c.name, projects.c.name).select_from(
        join_table).where(incomes.c.section_id == sections.c.id).where(incomes.c.project_id == projects.c.id).where(incomes.c.gave_person == income_gave_person)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No incomes Details Found with this Name: {income_gave_person}')
    data = build_incomes_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(IncomesResponse(**dict(data))))


@incomes_router.get('/get_income_by_check_number/{income_check_number}', response_model=IncomesResponse)
async def get_income_by_check_number(income_check_number: int, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = incomes.join(
        sections, incomes.c.section_id == sections.c.id).join(projects, incomes.c.project_id == projects.c.id)
    result = select(incomes, sections.c.name, projects.c.name).select_from(
        join_table).where(incomes.c.section_id == sections.c.id).where(incomes.c.project_id == projects.c.id).where(incomes.c.check_number == income_check_number)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No incomes Details Found with this Name: {income_check_number}')
    data = build_incomes_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(IncomesResponse(**dict(data))))


@incomes_router.get('/get_income_by_way_of_receiving/{income_way_of_receiving}', response_model=IncomesResponse)
async def get_income_by_way_of_receiving(income_way_of_receiving: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = incomes.join(
        sections, incomes.c.section_id == sections.c.id).join(projects, incomes.c.project_id == projects.c.id)
    result = select(incomes, sections.c.name, projects.c.name).select_from(
        join_table).where(incomes.c.section_id == sections.c.id).where(incomes.c.project_id == projects.c.id).where(incomes.c.way_of_receiving == income_way_of_receiving)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No incomes Details Found with this Name: {income_way_of_receiving}')
    data = build_incomes_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(IncomesResponse(**dict(data))))


@incomes_router.post('/', response_model=IncomesResponse)
async def insert_income(incomes_req: IncomesRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = incomes.insert().values(dict(incomes_req)).returning(ALL_COLUMNS)
    row_ = execute_one(result)
    if not row_:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='incomes Details Inserted failed')
    join_table = incomes.join(
        sections, incomes.c.section_id == sections.c.id).join(projects, incomes.c.project_id == projects.c.id)
    result = select(incomes, sections.c.name, projects.c.name).select_from(
        join_table).where(incomes.c.section_id == sections.c.id).where(incomes.c.project_id == projects.c.id).where(incomes.c.id == row_[0])
    row = execute_one(result)
    data = build_incomes_dict_post(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(IncomesResponse(**dict(data))))


@incomes_router.delete('/{income_id}', response_model=IncomesResponse)
async def delete_income(income_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = incomes.select().where(incomes.c.id == income_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No incomes Details Found with this ID: {income_id}')
    else:
        result = incomes.delete().where(
            incomes.c.id == income_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'incomes Deleted Failed with this ID: {income_id}')
        data = build_incomes_dict_post(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(IncomesResponse(**dict(data))))


@incomes_router.put('/{income_id}', response_model=IncomesResponse)
async def update_income(income_id: UUID, incomes_req: IncomesRequest, current_user: Login = Depends(get_current_user)):
    result = incomes.select().where(incomes.c.id == income_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No incomes Details Found with this ID: {income_id}')
    else:
        result = incomes.delete().where(
            incomes.c.id == income_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'incomes Deleted Failed with this ID: {income_id}')
        else:
            result = incomes.insert().values(dict(incomes_req)).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='incomes Details Updated failed')
            data = build_incomes_dict_post(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(IncomesResponse(**dict(data))))


@incomes_router.patch('/{income_id}', response_model=IncomesResponse)
async def update(income_id: UUID, incomes_req: IncomesRequest, current_user: Login = Depends(get_current_user)):
    result = incomes.select().where(incomes.c.id == income_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No incomes Details Found with this ID: {income_id}')
    else:
        result = incomes.update().where(incomes.c.id == income_id).values(
            dict(incomes_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='incomes Details Updated failed')
        data = build_incomes_dict_post(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(IncomesResponse(**dict(data))))
