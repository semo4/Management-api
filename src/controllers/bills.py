from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.database.database import ALL_COLUMNS
from uuid import UUID
from src.models.bills import bills
from src.types.users import Login
from src.models.projects import projects
from src.types.bills import BillsRequest, BillsResponse
from src.database.connection import execute_all, execute_one
from src.utils.helper import build_bills_dict, build_bills_post_dict
from sqlalchemy.sql import select
from src.auth.oauth2 import get_current_user


bills_router = APIRouter(prefix='/bills', tags=['Bills'])


@bills_router.get('/', response_model=BillsResponse)
async def get_bills(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    bills_list = list()
    join_table = bills.join(
        projects, bills.c.project_id == projects.c.id)
    res = select(bills, projects.c.name).select_from(
        join_table).where(bills.c.project_id == projects.c.id)
    result = execute_all(res)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No bills Details Found')
    for row in result:
        data = build_bills_dict(row)
        bills_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(BillsResponse(**dict(i)) for i in bills_list))


@bills_router.get('/get_bill/{bill_id}', response_model=BillsResponse)
async def get_bill(bill_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = bills.join(
        projects, bills.c.project_id == projects.c.id)
    result = select(bills, projects.c.name).select_from(join_table).where(
        bills.c.project_id == projects.c.id).where(bills.c.id == bill_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No bills Details Found with this ID: {bill_id}')
    data = build_bills_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(BillsResponse(**dict(data))))


@bills_router.get('/get_bill_by_store_name/{bill_store_name}', response_model=BillsResponse)
async def get_bill_by_name(bill_store_name: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = select(bills, projects.c.name).select_from(
        bills.join(projects, bills.c.project_id == projects.c.id)).where(
            bills.c.project_id == projects.c.id).where(bills.c.store_name == bill_store_name)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No bills Details Found with this Name: {bill_store_name}')
    data = build_bills_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(BillsResponse(**dict(data))))


@bills_router.get('/get_bill_by_buyer_name/{bill_buyer_name}', response_model=BillsResponse)
async def get_bill_by_buyer_name(bill_buyer_name: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = select(bills, projects.c.name).select_from(
        bills.join(projects, bills.c.project_id == projects.c.id)).where(
            bills.c.project_id == projects.c.id).where(bills.c.buyer_name == bill_buyer_name)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No bills Details Found with this Name: {bill_buyer_name}')
    data = build_bills_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(BillsResponse(**dict(data))))


@bills_router.get('/get_bill_by_bill_number/{bill_number}', response_model=BillsResponse)
async def get_bill_by_bill_number(bill_number: int, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = select(bills, projects.c.name).select_from(
        bills.join(projects, bills.c.project_id == projects.c.id)).where(
            bills.c.project_id == projects.c.id).where(bills.c.bill_number == bill_number)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No bills Details Found with this Name: {bill_number}')
    data = build_bills_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(BillsResponse(**dict(data))))


@bills_router.post('/', response_model=BillsResponse)
async def insert_bill(bills_req: BillsRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = bills.insert().values(dict(bills_req)).returning(ALL_COLUMNS)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='bills Details Inserted failed')
    data = build_bills_post_dict(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(BillsResponse(**dict(data))))


@bills_router.delete('/{bill_id}', response_model=BillsResponse)
async def delete_bill(bill_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = bills.select().where(bills.c.id == bill_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No bills Details Found with this ID: {bill_id}')
    else:
        result = bills.delete().where(
            bills.c.id == bill_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'bills Deleted Failed with this ID: {bill_id}')
        data = build_bills_post_dict(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(BillsResponse(**dict(data))))


@bills_router.put('/{bill_id}', response_model=BillsResponse)
async def update_bill(bill_id: UUID, bills_req: BillsRequest, current_user: Login = Depends(get_current_user)):
    result = bills.select().where(bills.c.id == bill_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No bills Details Found with this ID: {bill_id}')
    else:
        result = bills.delete().where(
            bills.c.id == bill_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'bills Deleted Failed with this ID: {bill_id}')
        else:
            result = bills.insert().values(dict(bills_req)).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='bills Details Updated failed')
            data = build_bills_post_dict(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(BillsResponse(**dict(data))))


@bills_router.patch('/{bill_id}', response_model=BillsResponse)
async def update(bill_id: UUID, bills_req: BillsRequest, current_user: Login = Depends(get_current_user)):
    result = bills.select().where(bills.c.id == bill_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No bills Details Found with this ID: {bill_id}')
    else:
        result = bills.update().where(bills.c.id == bill_id).values(
            dict(bills_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='bills Details Updated failed')
        data = build_bills_post_dict(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(BillsResponse(**dict(data))))
