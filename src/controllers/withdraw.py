from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.database.database import ALL_COLUMNS
from uuid import UUID
from src.models.withdraw import withdraw
from src.models.projects import projects
from src.models.sections import sections
from src.models.partners import partners
from src.types.withdraw import WithdrawRequest, WithdrawResponse
from src.database.connection import execute_all, execute_one
from src.utils.helper import build_withdraw_dict, build_withdraw_dict_post
from sqlalchemy.sql import select
from src.auth.oauth2 import get_current_user
from src.types.users import Login

withdraw_router = APIRouter(prefix='/withdraw', tags=['Withdraw'])


@withdraw_router.get('/', response_model=WithdrawResponse)
async def get_withdraws(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    withdraw_list = list()
    join_table = withdraw.join(
        sections, withdraw.c.section_id == sections.c.id).join(projects, withdraw.c.project_id == projects.c.id).join(partners, withdraw.c.partner_id == partners.c.id)
    res = select(withdraw, sections.c.name, projects.c.name, partners.c.name).select_from(
        join_table).where(withdraw.c.section_id == sections.c.id).where(withdraw.c.project_id == projects.c.id).where(withdraw.c.partner_id == partners.c.id)
    result = execute_all(res)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No withdraw Details Found')
    for row in result:
        data = build_withdraw_dict(row)
        withdraw_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(WithdrawResponse(**dict(i)) for i in withdraw_list))


@withdraw_router.get('/get_withdraw/{withdraw_id}', response_model=WithdrawResponse)
async def get_withdraw(withdraw_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = withdraw.join(
        sections, withdraw.c.section_id == sections.c.id).join(projects, withdraw.c.project_id == projects.c.id).join(partners, withdraw.c.partner_id == partners.c.id)
    result = select(withdraw, sections.c.name, projects.c.name, partners.c.name).select_from(
        join_table).where(withdraw.c.section_id == sections.c.id).where(withdraw.c.project_id == projects.c.id).where(withdraw.c.partner_id == partners.c.id).where(withdraw.c.id == withdraw_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No withdraw Details Found with this ID: {withdraw_id}')
    data = build_withdraw_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(WithdrawResponse(**dict(data))))


@withdraw_router.get('/get_withdraw_by_amount/{withdraw_amount}', response_model=WithdrawResponse)
async def get_withdraw_by_amount(withdraw_amount: float, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = withdraw.join(
        sections, withdraw.c.section_id == sections.c.id).join(
        projects, withdraw.c.project_id == projects.c.id).join(
        partners, withdraw.c.partner_id == partners.c.id)
    result = select(withdraw, sections.c.name, projects.c.name, partners.c.name).select_from(
        join_table).where(withdraw.c.section_id == sections.c.id).where(
            withdraw.c.project_id == projects.c.id).where(
            withdraw.c.partner_id == partners.c.id).where(
            withdraw.c.amount == withdraw_amount)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No withdraw Details Found with this ID: {withdraw_amount}')
    data = build_withdraw_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(WithdrawResponse(**dict(data))))


@withdraw_router.post('/', response_model=WithdrawResponse)
async def insert_withdraw(withdraw_req: WithdrawRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = withdraw.insert().values(
        dict(withdraw_req)).returning(ALL_COLUMNS)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='withdraw Details Inserted failed')
    data = build_withdraw_dict_post(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(WithdrawResponse(**dict(data))))


@withdraw_router.delete('/{withdraw_id}', response_model=WithdrawResponse)
async def delete_withdraw(withdraw_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = withdraw.select().where(
        withdraw.c.id == withdraw_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No withdraw Details Found with this ID: {withdraw_id}')
    else:
        result = withdraw.delete().where(
            withdraw.c.id == withdraw_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'withdraw Deleted Failed with this ID: {withdraw_id}')
        data = build_withdraw_dict_post(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(WithdrawResponse(**dict(data))))


@withdraw_router.put('/{withdraw_id}', response_model=WithdrawResponse)
async def update_withdraw(withdraw_id: UUID, withdraw_req: WithdrawRequest, current_user: Login = Depends(get_current_user)):
    result = withdraw.select().where(
        withdraw.c.id == withdraw_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No withdraw Details Found with this ID: {withdraw_id}')
    else:
        result = withdraw.delete().where(
            withdraw.c.id == withdraw_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'withdraw Deleted Failed with this ID: {withdraw_id}')
        else:
            result = withdraw.insert().values(
                dict(withdraw_req)).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='withdraw Details Updated failed')
            data = build_withdraw_dict_post(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(WithdrawResponse(**dict(data))))


@withdraw_router.patch('/{withdraw_id}', response_model=WithdrawResponse)
async def update(withdraw_id: UUID, withdraw_req: WithdrawRequest, current_user: Login = Depends(get_current_user)):
    result = withdraw.select().where(
        withdraw.c.id == withdraw_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No withdraw Details Found with this ID: {withdraw_id}')
    else:
        result = withdraw.update().where(withdraw.c.id == withdraw_id).values(
            dict(withdraw_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='withdraw Details Updated failed')
        data = build_withdraw_dict_post(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(WithdrawResponse(**dict(data))))
