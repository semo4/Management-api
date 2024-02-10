from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.database.database import ALL_COLUMNS
from uuid import UUID
from src.models.projects import projects
from src.models.outcomes_categories import categories
from src.models.outcomes import outcomes
from src.types.outcomes import OutcomesRequest, OutcomesResponse
from src.database.connection import execute_all, execute_one
from src.utils.helper import build_outcomes_dict, build_outcomes_dict_post
from sqlalchemy.sql import select
from datetime import datetime
from src.auth.oauth2 import get_current_user
from src.types.users import Login


outcomes_router = APIRouter(prefix='/outcomes', tags=['Outcomes'])


@outcomes_router.get('/', response_model=OutcomesResponse)
async def get_outcomes(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    outcomes_list = list()
    join_table = outcomes.join(
        categories, outcomes.c.category_id == categories.c.id).join(projects, outcomes.c.project_id == projects.c.id)
    res = select(outcomes, categories.c.title, projects.c.name).select_from(
        join_table).where(outcomes.c.category_id == categories.c.id).where(outcomes.c.project_id == projects.c.id)
    result = execute_all(res)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No outcomes Details Found')
    for row in result:
        data = build_outcomes_dict(row)
        outcomes_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(OutcomesResponse(**dict(i)) for i in outcomes_list))


@outcomes_router.get('/get_outcome/{outcome_id}', response_model=OutcomesResponse)
async def get_outcome(outcome_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = outcomes.join(
        categories, outcomes.c.category_id == categories.c.id).join(projects, outcomes.c.project_id == projects.c.id)
    result = select(outcomes, categories.c.title, projects.c.name).select_from(
        join_table).where(outcomes.c.category_id == categories.c.id).where(outcomes.c.project_id == projects.c.id).where(outcomes.c.id == outcome_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No outcomes Details Found with this ID: {outcome_id}')
    data = build_outcomes_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(OutcomesResponse(**dict(data, exclude_none=True))))


@outcomes_router.get('/get_outcome_by_buyer_name/{outcome_buyer_name}', response_model=OutcomesResponse)
async def get_outcome_by_buyer_name(outcome_buyer_name: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = outcomes.join(
        categories, outcomes.c.category_id == categories.c.id).join(projects, outcomes.c.project_id == projects.c.id)
    result = select(outcomes, categories.c.title, projects.c.name).select_from(
        join_table).where(outcomes.c.category_id == categories.c.id).where(outcomes.c.project_id == projects.c.id).where(outcomes.c.buyer_name == outcome_buyer_name)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No outcomes Details Found with this Name: {outcome_buyer_name}')
    data = build_outcomes_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(OutcomesResponse(**dict(data))))


@outcomes_router.get('/get_outcome_by_amount_payed/{outcome_amount_payed}', response_model=OutcomesResponse)
async def get_outcome_by_amount_payed(outcome_amount_payed: float, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = outcomes.join(
        categories, outcomes.c.category_id == categories.c.id).join(projects, outcomes.c.project_id == projects.c.id)
    result = select(outcomes, categories.c.title, projects.c.name).select_from(
        join_table).where(outcomes.c.category_id == categories.c.id).where(outcomes.c.project_id == projects.c.id).where(outcomes.c.amount_payed == outcome_amount_payed)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No outcomes Details Found with this Name: {outcome_amount_payed}')
    data = build_outcomes_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(OutcomesResponse(**dict(data))))


@outcomes_router.get('/get_outcome_by_date/{outcome_date}', response_model=OutcomesResponse)
async def get_outcome_by_date(outcome_date: datetime, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = outcomes.join(
        categories, outcomes.c.category_id == categories.c.id).join(projects, outcomes.c.project_id == projects.c.id)
    result = select(outcomes, categories.c.title, projects.c.name).select_from(
        join_table).where(outcomes.c.category_id == categories.c.id).where(outcomes.c.project_id == projects.c.id).where(outcomes.c.date == outcome_date)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No outcomes Details Found with this Name: {outcome_date}')
    data = build_outcomes_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(OutcomesResponse(**dict(data))))


@outcomes_router.post('/', response_model=OutcomesResponse)
async def insert_outcome(outcomes_req: OutcomesRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = outcomes.insert().values(dict(outcomes_req)).returning(ALL_COLUMNS)
    row_ = execute_one(result)
    if not row_:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='outcomes Details Inserted failed')
    join_table = outcomes.join(
        categories, outcomes.c.category_id == categories.c.id).join(projects, outcomes.c.project_id == projects.c.id)
    result = select(outcomes, categories.c.title, projects.c.name).select_from(
        join_table).where(outcomes.c.category_id == categories.c.id).where(outcomes.c.project_id == projects.c.id).where(outcomes.c.id == row_[0])
    row = execute_one(result)
    data = build_outcomes_dict_post(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(OutcomesResponse(**dict(data))))


@outcomes_router.delete('/{outcome_id}', response_model=OutcomesResponse)
async def delete_outcome(outcome_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = outcomes.select().where(outcomes.c.id == outcome_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No outcomes Details Found with this ID: {outcome_id}')
    else:
        result = outcomes.delete().where(
            outcomes.c.id == outcome_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'outcomes Deleted Failed with this ID: {outcome_id}')
        data = build_outcomes_dict_post(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(OutcomesResponse(**dict(data))))


@outcomes_router.put('/{outcome_id}', response_model=OutcomesResponse)
async def update_outcome(outcome_id: UUID, outcomes_req: OutcomesRequest, current_user: Login = Depends(get_current_user)):
    result = outcomes.select().where(outcomes.c.id == outcome_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No outcomes Details Found with this ID: {outcome_id}')
    else:
        result = outcomes.delete().where(
            outcomes.c.id == outcome_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'outcomes Deleted Failed with this ID: {outcome_id}')
        else:
            result = outcomes.insert().values(dict(outcomes_req)).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='outcomes Details Updated failed')
            data = build_outcomes_dict_post(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(OutcomesResponse(**dict(data))))


@outcomes_router.patch('/{outcome_id}', response_model=OutcomesResponse)
async def update(outcome_id: UUID, outcomes_req: OutcomesRequest, current_user: Login = Depends(get_current_user)):
    result = outcomes.select().where(outcomes.c.id == outcome_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No outcomes Details Found with this ID: {outcome_id}')
    else:
        result = outcomes.update().where(outcomes.c.id == outcome_id).values(
            dict(outcomes_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='outcomes Details Updated failed')
        data = build_outcomes_dict_post(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(OutcomesResponse(**dict(data))))
