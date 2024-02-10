from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.database.database import ALL_COLUMNS
from uuid import UUID
from src.models.outcomes_categories import categories
from src.types.outcomes_categories import OutcomesCategoriesRequest, OutcomesCategoriesResponse
from src.database.connection import execute_all, execute_one
from src.utils.helper import build_response_dict
from src.auth.oauth2 import get_current_user
from src.types.users import Login

categories_router = APIRouter(prefix='/categories', tags=['Categories'])


@categories_router.get('/', response_model=OutcomesCategoriesResponse)
async def get_categories(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    categories_list = list()
    result = execute_all(categories.select())
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No categories Details Found')
    for row in result:
        data = build_response_dict(row)
        categories_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(OutcomesCategoriesResponse(**dict(i)) for i in categories_list))


@categories_router.get('/get_categories/{categories_id}', response_model=OutcomesCategoriesResponse)
async def get_category(categories_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = categories.select().where(categories.c.id == categories_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No categories Details Found with this ID: {categories_id}')
    data = build_response_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(OutcomesCategoriesResponse(**dict(data))))


@categories_router.get('/get_categories_by_title/{categories_title}', response_model=OutcomesCategoriesResponse)
async def get_categories_by_title(categories_title: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = categories.select().where(categories.c.title == categories_title)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No categories Details Found with this Name: {categories_title}')
    data = build_response_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(OutcomesCategoriesResponse(**dict(data))))


@categories_router.post('/', response_model=OutcomesCategoriesResponse)
async def insert_categories(categories_req: OutcomesCategoriesRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = categories.insert().values(dict(categories_req)).returning(ALL_COLUMNS)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='categories Details Inserted failed')
    data = build_response_dict(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(OutcomesCategoriesResponse(**dict(data))))


@categories_router.delete('/{categories_id}', response_model=OutcomesCategoriesResponse)
async def delete_categories(categories_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = categories.select().where(categories.c.id == categories_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No categories Details Found with this ID: {categories_id}')
    else:
        result = categories.delete().where(
            categories.c.id == categories_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'categories Deleted Failed with this ID: {categories_id}')
        data = build_response_dict(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(OutcomesCategoriesResponse(**dict(data))))


@categories_router.put('/{categories_id}', response_model=OutcomesCategoriesResponse)
async def update_categories(categories_id: UUID, categories_req: OutcomesCategoriesRequest, current_user: Login = Depends(get_current_user)):
    result = categories.select().where(categories.c.id == categories_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No categories Details Found with this ID: {categories_id}')
    else:
        result = categories.delete().where(
            categories.c.id == categories_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'categories Deleted Failed with this ID: {categories_id}')
        else:
            result = categories.insert().values(dict(categories_req)).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='categories Details Updated failed')
            data = build_response_dict(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(OutcomesCategoriesResponse(**dict(data))))


@categories_router.patch('/{categories_id}', response_model=OutcomesCategoriesResponse)
async def update(categories_id: UUID, categories_req: OutcomesCategoriesRequest, current_user: Login = Depends(get_current_user)):
    result = categories.select().where(categories.c.id == categories_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No categories Details Found with this ID: {categories_id}')
    else:
        result = categories.update().where(categories.c.id == categories_id).values(
            dict(categories_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='categories Details Updated failed')
        data = build_response_dict(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(OutcomesCategoriesResponse(**dict(data))))
