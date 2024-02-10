from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.database.database import ALL_COLUMNS
from uuid import UUID
from src.models.workplaces import workplace
from src.types.workplaces import WorkPlacesRequest, WorkPlacesResponse
from src.database.connection import execute_all, execute_one
from src.utils.helper import build_response_dict
from src.auth.oauth2 import get_current_user
from src.types.users import Login

workplace_router = APIRouter(prefix='/workplace', tags=['WorkPlace'])


@workplace_router.get('/', response_model=WorkPlacesResponse)
async def get_workplaces(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    workplace_list = list()
    result = execute_all(workplace.select())
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No workplace Details Found')
    for row in result:
        data = build_response_dict(row)
        workplace_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(WorkPlacesResponse(**dict(i)) for i in workplace_list))


@workplace_router.get('/get_workplace/{workplace_id}', response_model=WorkPlacesResponse)
async def get_workplace(workplace_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = workplace.select().where(workplace.c.id == workplace_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No workplace Details Found with this ID: {workplace_id}')
    data = build_response_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(WorkPlacesResponse(**dict(data))))


@workplace_router.get('/get_workplace_by_title/{workplace_title}', response_model=WorkPlacesResponse)
async def get_workplace_by_title(workplace_title: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = workplace.select().where(workplace.c.title == workplace_title)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No workplace Details Found with this Name: {workplace_title}')
    data = build_response_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(WorkPlacesResponse(**dict(data))))


@workplace_router.post('/', response_model=WorkPlacesResponse)
async def insert_workplace(workplace_req: WorkPlacesRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = workplace.insert().values(dict(workplace_req)).returning(ALL_COLUMNS)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='workplace Details Inserted failed')
    data = build_response_dict(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(WorkPlacesResponse(**dict(data))))


@workplace_router.delete('/{workplace_id}', response_model=WorkPlacesResponse)
async def delete_workplace(workplace_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = workplace.select().where(workplace.c.id == workplace_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No workplace Details Found with this ID: {workplace_id}')
    else:
        result = workplace.delete().where(
            workplace.c.id == workplace_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'workplace Deleted Failed with this ID: {workplace_id}')
        data = build_response_dict(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(WorkPlacesResponse(**dict(data))))


@workplace_router.put('/{workplace_id}', response_model=WorkPlacesResponse)
async def update_workplace(workplace_id: UUID, workplace_req: WorkPlacesRequest, current_user: Login = Depends(get_current_user)):
    result = workplace.select().where(workplace.c.id == workplace_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No workplace Details Found with this ID: {workplace_id}')
    else:
        result = workplace.delete().where(
            workplace.c.id == workplace_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'workplace Deleted Failed with this ID: {workplace_id}')
        else:
            result = workplace.insert().values(dict(workplace_req)).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='workplace Details Updated failed')
            data = build_response_dict(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(WorkPlacesResponse(**dict(data))))


@workplace_router.patch('/{workplace_id}', response_model=WorkPlacesResponse)
async def update(workplace_id: UUID, workplace_req: WorkPlacesRequest, current_user: Login = Depends(get_current_user)):
    result = workplace.select().where(workplace.c.id == workplace_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No workplace Details Found with this ID: {workplace_id}')
    else:
        result = workplace.update().where(workplace.c.id == workplace_id).values(
            dict(workplace_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='workplace Details Updated failed')
        data = build_response_dict(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(WorkPlacesResponse(**dict(data))))
