from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.database.database import ALL_COLUMNS
from uuid import UUID
from src.models.covenants import covenants_cash, covenants_devices
from src.models.partners import partners
from src.models.workers import workers
from src.types.covenants import CovenantsCashResponse, CovenantsCashRequest, CovenantsDevicesRequest, CovenantsDevicesResponse
from src.database.connection import execute_all, execute_one
from src.utils.helper import build_covenants_cash_dict, build_covenants_cash_post_dict, build_covenants_devices_dict, build_covenants_devices_post_dict
from sqlalchemy.sql import select
from src.auth.oauth2 import get_current_user
from src.types.users import Login


covenants_cash_router = APIRouter(
    prefix='/covenants_cash', tags=['Covenants Cash'])


@covenants_cash_router.get('/', response_model=CovenantsCashResponse)
async def get_covenants_cash(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    covenants_cash_list = list()
    join_table = covenants_cash.join(
        partners, covenants_cash.c.partner_id == partners.c.id)
    res = select(covenants_cash, partners.c.name).select_from(
        join_table).where(covenants_cash.c.partner_id == partners.c.id)
    result = execute_all(res)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No Covenants Cash Details Found')
    for row in result:
        data = build_covenants_cash_dict(row)
        covenants_cash_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(CovenantsCashResponse(**dict(i)) for i in covenants_cash_list))


@covenants_cash_router.get('/get_covenant_cash/{covenant_cash_id}', response_model=CovenantsCashResponse)
async def get_covenant_cash(covenant_cash_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = covenants_cash.join(
        partners, covenants_cash.c.partner_id == partners.c.id)
    result = select(covenants_cash, partners.c.name).select_from(join_table).where(
        covenants_cash.c.partner_id == partners.c.id).where(covenants_cash.c.id == covenant_cash_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No Covenants Cash Details Found with this ID: {covenant_cash_id}')
    data = build_covenants_cash_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(CovenantsCashResponse(**dict(data))))


@covenants_cash_router.get('/get_covenant_cash_by_name/{covenant_cash_name}', response_model=CovenantsCashResponse)
async def get_covenant_cash_by_name(covenant_cash_name: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = select(covenants_cash, partners.c.name).select_from(
        covenants_cash.join(partners, covenants_cash.c.partner_id == partners.c.id)).where(
            covenants_cash.c.partner_id == partners.c.id).where(covenants_cash.c.name == covenant_cash_name)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No Covenants Cash Details Found with this Name: {covenant_cash_name}')
    data = build_covenants_cash_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(CovenantsCashResponse(**dict(data))))


@covenants_cash_router.post('/', response_model=CovenantsCashResponse)
async def insert_covenant_cash(covenants_cash_req: CovenantsCashRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = covenants_cash.insert().values(
        dict(covenants_cash_req)).returning(ALL_COLUMNS)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Covenants Cash Details Inserted failed')
    data = build_covenants_cash_post_dict(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(CovenantsCashResponse(**dict(data))))


@covenants_cash_router.delete('/{covenant_cash_id}', response_model=CovenantsCashResponse)
async def delete_covenant_cash(covenant_cash_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = covenants_cash.select().where(covenants_cash.c.id == covenant_cash_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No Covenants Cash Details Found with this ID: {covenant_cash_id}')
    else:
        result = covenants_cash.delete().where(
            covenants_cash.c.id == covenant_cash_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'covenants_cash Deleted Failed with this ID: {covenant_cash_id}')
        data = build_covenants_cash_post_dict(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(CovenantsCashResponse(**dict(data))))


@covenants_cash_router.put('/{covenant_cash_id}', response_model=CovenantsCashResponse)
async def update_covenant_cash(covenant_cash_id: UUID, covenants_cash_req: CovenantsCashRequest, current_user: Login = Depends(get_current_user)):
    result = covenants_cash.select().where(covenants_cash.c.id == covenant_cash_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No Covenants Cash Details Found with this ID: {covenant_cash_id}')
    else:
        result = covenants_cash.delete().where(
            covenants_cash.c.id == covenant_cash_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'covenants_cash Deleted Failed with this ID: {covenant_cash_id}')
        else:
            result = covenants_cash.insert().values(
                dict(covenants_cash_req)).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='Covenants Cash Details Updated failed')
            data = build_covenants_cash_post_dict(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(CovenantsCashResponse(**dict(data))))


@covenants_cash_router.patch('/{covenant_cash_id}', response_model=CovenantsCashResponse)
async def update(covenant_cash_id: UUID, covenants_cash_req: CovenantsCashRequest, current_user: Login = Depends(get_current_user)):
    result = covenants_cash.select().where(covenants_cash.c.id == covenant_cash_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No Covenants Cash Details Found with this ID: {covenant_cash_id}')
    else:
        result = covenants_cash.update().where(covenants_cash.c.id == covenant_cash_id).values(
            dict(covenants_cash_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Covenants Cash Details Updated failed')
        data = build_covenants_cash_post_dict(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(CovenantsCashResponse(**dict(data))))


covenants_devices_router = APIRouter(
    prefix='/covenants_device', tags=['Covenants Device'])


@covenants_devices_router.get('/', response_model=CovenantsDevicesResponse)
async def get_covenants_devices(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    covenants_devices_list = list()
    join_table = covenants_devices.join(
        workers, covenants_devices.c.worker_id == workers.c.id)
    res = select(covenants_devices, workers.c.name).select_from(
        join_table).where(covenants_devices.c.worker_id == workers.c.id)
    result = execute_all(res)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No Covenants Devices Details Found')
    for row in result:
        data = build_covenants_devices_dict(row)
        covenants_devices_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(CovenantsDevicesResponse(**dict(i)) for i in covenants_devices_list))


@covenants_devices_router.get('/get_covenant_device/{covenant_device_id}', response_model=CovenantsDevicesResponse)
async def get_covenant_device(covenant_device_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = covenants_devices.join(
        workers, covenants_devices.c.worker_id == workers.c.id)
    result = select(covenants_devices, workers.c.name).select_from(join_table).where(
        covenants_devices.c.worker_id == workers.c.id).where(covenants_devices.c.id == covenant_device_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No Covenants Devices Details Found with this ID: {covenant_device_id}')
    data = build_covenants_devices_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(CovenantsDevicesResponse(**dict(data))))


@covenants_devices_router.get('/get_covenant_device_by_name/{covenant_device_name}', response_model=CovenantsDevicesResponse)
async def get_covenant_device_by_name(covenant_device_name: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = select(covenants_devices, workers.c.name).select_from(
        covenants_devices.join(workers, covenants_devices.c.worker_id == workers.c.id)).where(
            covenants_devices.c.worker_id == workers.c.id).where(covenants_devices.c.title == covenant_device_name)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No Covenants Devices Details Found with this Name: {covenant_device_name}')
    data = build_covenants_devices_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(CovenantsDevicesResponse(**dict(data))))


@covenants_devices_router.post('/', response_model=CovenantsDevicesResponse)
async def insert_covenant_device(covenants_devices_req: CovenantsDevicesRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = covenants_devices.insert().values(
        dict(covenants_devices_req)).returning(ALL_COLUMNS)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Covenants Devices Details Inserted failed')
    data = build_covenants_devices_post_dict(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(CovenantsDevicesResponse(**dict(data))))


@covenants_devices_router.delete('/{covenant_device_id}', response_model=CovenantsDevicesResponse)
async def delete_covenant_device(covenant_device_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = covenants_devices.select().where(
        covenants_devices.c.id == covenant_device_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No Covenants Devices Details Found with this ID: {covenant_device_id}')
    else:
        result = covenants_devices.delete().where(
            covenants_devices.c.id == covenant_device_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'covenants_devices Deleted Failed with this ID: {covenant_device_id}')
        data = build_covenants_devices_post_dict(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(CovenantsDevicesResponse(**dict(data))))


@covenants_devices_router.put('/{covenant_device_id}', response_model=CovenantsDevicesResponse)
async def update_covenant_device(covenant_device_id: UUID, covenants_devices_req: CovenantsDevicesRequest, current_user: Login = Depends(get_current_user)):
    result = covenants_devices.select().where(
        covenants_devices.c.id == covenant_device_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No Covenants Devices Details Found with this ID: {covenant_device_id}')
    else:
        result = covenants_devices.delete().where(
            covenants_devices.c.id == covenant_device_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'covenants_devices Deleted Failed with this ID: {covenant_device_id}')
        else:
            result = covenants_devices.insert().values(
                dict(covenants_devices_req)).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='Covenants Devices Details Updated failed')
            data = build_covenants_devices_post_dict(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(CovenantsDevicesResponse(**dict(data))))


@covenants_devices_router.patch('/{covenant_device_id}', response_model=CovenantsDevicesResponse)
async def update_device(covenant_device_id: UUID, covenants_devices_req: CovenantsDevicesRequest, current_user: Login = Depends(get_current_user)):
    result = covenants_devices.select().where(
        covenants_devices.c.id == covenant_device_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No Covenants Devices Details Found with this ID: {covenant_device_id}')
    else:
        result = covenants_devices.update().where(covenants_devices.c.id == covenant_device_id).values(
            dict(covenants_devices_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Covenants Devices Details Updated failed')
        data = build_covenants_devices_post_dict(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(CovenantsDevicesResponse(**dict(data))))
