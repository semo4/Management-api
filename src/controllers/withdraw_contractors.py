from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.database.database import ALL_COLUMNS
from uuid import UUID
from src.models.withdraw_contractors import withdraw_contractors
from src.models.projects import projects
from src.models.sections import sections
from src.models.contractors import contractors
from src.types.withdraw_contractors import WithdrawContractorsRequest, WithdrawContractorsResponse
from src.database.connection import execute_all, execute_one
from src.utils.helper import build_withdraw_contractors_dict, build_withdraw_contractors_dict_post
from sqlalchemy.sql import select
from src.auth.oauth2 import get_current_user
from src.types.users import Login


withdraw_contractors_router = APIRouter(
    prefix='/withdraw_contractors', tags=['Withdraw Contractors'])


@withdraw_contractors_router.get('/', response_model=WithdrawContractorsResponse)
async def get_withdraw_contractors(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    withdraw_contractors_list = list()
    join_table = withdraw_contractors.join(
        sections, withdraw_contractors.c.section_id == sections.c.id).join(projects, withdraw_contractors.c.project_id == projects.c.id).join(contractors, withdraw_contractors.c.contractor_id == contractors.c.id)
    res = select(withdraw_contractors, sections.c.name, projects.c.name, contractors.c.name).select_from(
        join_table).where(withdraw_contractors.c.section_id == sections.c.id).where(withdraw_contractors.c.project_id == projects.c.id).where(withdraw_contractors.c.contractor_id == contractors.c.id)
    result = execute_all(res)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No withdraw_contractors Details Found')
    for row in result:
        data = build_withdraw_contractors_dict(row)
        withdraw_contractors_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(WithdrawContractorsResponse(**dict(i)) for i in withdraw_contractors_list))


@withdraw_contractors_router.get('/get_operation/{withdraw_contractors_id}', response_model=WithdrawContractorsResponse)
async def get_operation(withdraw_contractors_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = withdraw_contractors.join(
        sections, withdraw_contractors.c.section_id == sections.c.id).join(projects, withdraw_contractors.c.project_id == projects.c.id).join(contractors, withdraw_contractors.c.contractor_id == contractors.c.id)
    result = select(withdraw_contractors, sections.c.name, projects.c.name, contractors.c.name).select_from(
        join_table).where(withdraw_contractors.c.section_id == sections.c.id).where(withdraw_contractors.c.project_id == projects.c.id).where(withdraw_contractors.c.contractor_id == contractors.c.id).where(withdraw_contractors.c.id == withdraw_contractors_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No withdraw_contractors Details Found with this ID: {withdraw_contractors_id}')
    data = build_withdraw_contractors_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(WithdrawContractorsResponse(**dict(data))))


@withdraw_contractors_router.get('/get_operation_by_amount/{withdraw_contractors_amount}', response_model=WithdrawContractorsResponse)
async def get_operation_by_amount(withdraw_contractors_amount: float, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = withdraw_contractors.join(
        sections, withdraw_contractors.c.section_id == sections.c.id).join(
        projects, withdraw_contractors.c.project_id == projects.c.id).join(
        contractors, withdraw_contractors.c.contractor_id == contractors.c.id)
    result = select(withdraw_contractors, sections.c.name, projects.c.name, contractors.c.name).select_from(
        join_table).where(withdraw_contractors.c.section_id == sections.c.id).where(
            withdraw_contractors.c.project_id == projects.c.id).where(
            withdraw_contractors.c.contractor_id == contractors.c.id).where(
            withdraw_contractors.c.amount == withdraw_contractors_amount)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No withdraw_contractors Details Found with this ID: {withdraw_contractors_amount}')
    data = build_withdraw_contractors_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(WithdrawContractorsResponse(**dict(data))))


@withdraw_contractors_router.post('/', response_model=WithdrawContractorsResponse)
async def insert_operation(withdraw_contractors_req: WithdrawContractorsRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = withdraw_contractors.insert().values(
        dict(withdraw_contractors_req)).returning(ALL_COLUMNS)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='withdraw_contractors Details Inserted failed')
    data = build_withdraw_contractors_dict_post(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(WithdrawContractorsResponse(**dict(data))))


@withdraw_contractors_router.delete('/{withdraw_contractors_id}', response_model=WithdrawContractorsResponse)
async def delete_withdraw_contractors(withdraw_contractors_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = withdraw_contractors.select().where(
        withdraw_contractors.c.id == withdraw_contractors_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No withdraw_contractors Details Found with this ID: {withdraw_contractors_id}')
    else:
        result = withdraw_contractors.delete().where(
            withdraw_contractors.c.id == withdraw_contractors_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'withdraw_contractors Deleted Failed with this ID: {withdraw_contractors_id}')
        data = build_withdraw_contractors_dict_post(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(WithdrawContractorsResponse(**dict(data))))


@withdraw_contractors_router.put('/{withdraw_contractors_id}', response_model=WithdrawContractorsResponse)
async def update_withdraw_contractors(withdraw_contractors_id: UUID, withdraw_contractors_req: WithdrawContractorsRequest, current_user: Login = Depends(get_current_user)):
    result = withdraw_contractors.select().where(
        withdraw_contractors.c.id == withdraw_contractors_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No withdraw_contractors Details Found with this ID: {withdraw_contractors_id}')
    else:
        result = withdraw_contractors.delete().where(
            withdraw_contractors.c.id == withdraw_contractors_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'withdraw_contractors Deleted Failed with this ID: {withdraw_contractors_id}')
        else:
            result = withdraw_contractors.insert().values(
                dict(withdraw_contractors_req)).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='withdraw_contractors Details Updated failed')
            data = build_withdraw_contractors_dict_post(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(WithdrawContractorsResponse(**dict(data))))


@withdraw_contractors_router.patch('/{withdraw_contractors_id}', response_model=WithdrawContractorsResponse)
async def update(withdraw_contractors_id: UUID, withdraw_contractors_req: WithdrawContractorsRequest, current_user: Login = Depends(get_current_user)):
    result = withdraw_contractors.select().where(
        withdraw_contractors.c.id == withdraw_contractors_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No withdraw_contractors Details Found with this ID: {withdraw_contractors_id}')
    else:
        result = withdraw_contractors.update().where(withdraw_contractors.c.id == withdraw_contractors_id).values(
            dict(withdraw_contractors_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='withdraw_contractors Details Updated failed')
        data = build_withdraw_contractors_dict_post(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(WithdrawContractorsResponse(**dict(data))))
