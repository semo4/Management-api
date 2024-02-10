from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.database.database import ALL_COLUMNS
from uuid import UUID
from src.models.projects import projects
from src.models.sections import sections
from src.models.contractors import contractors
from src.types.contractors import ContractorsRequest, ContractorsResponse
from src.database.connection import execute_all, execute_one
from src.utils.helper import build_contractors_dict, build_contractors_dict_post
from src.utils.calculation import calculation_contractors
from sqlalchemy.sql import select
from src.auth.oauth2 import get_current_user
from src.types.users import Login

contractors_router = APIRouter(prefix='/contractors', tags=['Contractors'])


@contractors_router.get('/', response_model=ContractorsResponse)
async def get_contractors(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    contractors_list = list()
    join_table = contractors.join(
        sections, contractors.c.section_id == sections.c.id).join(projects, contractors.c.project_id == projects.c.id)
    res = select(contractors, sections.c.name, projects.c.name).select_from(
        join_table).where(contractors.c.section_id == sections.c.id).where(contractors.c.project_id == projects.c.id)
    result = execute_all(res)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No contractors Details Found')
    for row in result:
        data = build_contractors_dict(row)
        contractors_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(ContractorsResponse(**dict(i)) for i in contractors_list))


@contractors_router.get('/get_contractor/{contractor_id}', response_model=ContractorsResponse)
async def get_contractor(contractor_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = contractors.join(
        sections, contractors.c.section_id == sections.c.id).join(projects, contractors.c.project_id == projects.c.id)
    result = select(contractors, sections.c.name, projects.c.name).select_from(
        join_table).where(contractors.c.section_id == sections.c.id).where(contractors.c.project_id == projects.c.id).where(contractors.c.id == contractor_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No contractors Details Found with this ID: {contractor_id}')
    data = build_contractors_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(ContractorsResponse(**dict(data, exclude_none=True))))


@contractors_router.get('/get_contractor_by_name/{contractor_name}', response_model=ContractorsResponse)
async def get_contractor_by_name(contractor_name: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = contractors.join(
        sections, contractors.c.section_id == sections.c.id).join(projects, contractors.c.project_id == projects.c.id)
    result = select(contractors, sections.c.name, projects.c.name).select_from(
        join_table).where(contractors.c.section_id == sections.c.id).where(contractors.c.project_id == projects.c.id).where(contractors.c.name == contractor_name)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No contractors Details Found with this Name: {contractor_name}')
    data = build_contractors_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(ContractorsResponse(**dict(data))))


@contractors_router.post('/', response_model=ContractorsResponse)
async def insert_contractor(contractors_req: ContractorsRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    calculated_data = calculation_contractors(dict(contractors_req))
    result = contractors.insert().values(calculated_data).returning(ALL_COLUMNS)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='contractors Details Inserted failed')
    data = build_contractors_dict_post(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(ContractorsResponse(**dict(data))))


@contractors_router.delete('/{contractor_id}', response_model=ContractorsResponse)
async def delete_contractor(contractor_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = contractors.select().where(contractors.c.id == contractor_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No contractors Details Found with this ID: {contractor_id}')
    else:
        result = contractors.delete().where(
            contractors.c.id == contractor_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'contractors Deleted Failed with this ID: {contractor_id}')
        data = build_contractors_dict_post(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(ContractorsResponse(**dict(data))))


@contractors_router.put('/{contractor_id}', response_model=ContractorsResponse)
async def update_contractor(contractor_id: UUID, contractors_req: ContractorsRequest, current_user: Login = Depends(get_current_user)):
    result = contractors.select().where(contractors.c.id == contractor_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No contractors Details Found with this ID: {contractor_id}')
    else:
        result = contractors.delete().where(
            contractors.c.id == contractor_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'contractors Deleted Failed with this ID: {contractor_id}')
        else:
            calculated_data = calculation_contractors(dict(contractors_req))
            result = contractors.insert().values(calculated_data).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='contractors Details Updated failed')
            data = build_contractors_dict_post(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(ContractorsResponse(**dict(data))))


@contractors_router.patch('/{contractor_id}', response_model=ContractorsResponse)
async def update(contractor_id: UUID, contractors_req: ContractorsRequest, current_user: Login = Depends(get_current_user)):
    result = contractors.select().where(contractors.c.id == contractor_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No contractors Details Found with this ID: {contractor_id}')
    else:
        calculated_data = calculation_contractors(
            dict(contractors_req.dict(exclude_unset=True)))
        result = contractors.update().where(contractors.c.id == contractor_id).values(
            calculated_data).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='contractors Details Updated failed')
        data = build_contractors_dict_post(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(ContractorsResponse(**dict(data))))
