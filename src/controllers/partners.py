from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.database.database import ALL_COLUMNS
from uuid import UUID
from src.models.partners import partners
from src.models.sections import sections
from src.types.partners import PartnersRequest, PartnersResponse
from src.database.connection import execute_all, execute_one
from src.utils.helper import build_partners_dict, build_partners_post_dict
from sqlalchemy.sql import select
from src.auth.oauth2 import get_current_user
from src.types.users import Login

partners_router = APIRouter(prefix='/partners', tags=['Partners'])


@partners_router.get('/', response_model=PartnersResponse)
async def get_partners(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    partners_list = list()
    join_table = partners.join(
        sections, partners.c.section_id == sections.c.id)
    res = select(partners, sections.c.name).select_from(
        join_table).where(partners.c.section_id == sections.c.id)
    result = execute_all(res)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No partners Details Found')
    for row in result:
        data = build_partners_dict(row)
        partners_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(PartnersResponse(**dict(i)) for i in partners_list))


@partners_router.get('/get_partner/{partner_id}', response_model=PartnersResponse)
async def get_partner(partner_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = partners.join(
        sections, partners.c.section_id == sections.c.id)
    result = select(partners, sections.c.name).select_from(join_table).where(
        partners.c.section_id == sections.c.id).where(partners.c.id == partner_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No partners Details Found with this ID: {partner_id}')
    data = build_partners_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(PartnersResponse(**dict(data))))


@partners_router.get('/get_partner_by_name/{partner_name}', response_model=PartnersResponse)
async def get_partner_by_name(partner_name: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = select(partners, sections.c.name).select_from(
        partners.join(sections, partners.c.section_id == sections.c.id)).where(
            partners.c.section_id == sections.c.id).where(partners.c.name == partner_name)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No partners Details Found with this Name: {partner_name}')
    data = build_partners_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(PartnersResponse(**dict(data))))


@partners_router.post('/', response_model=PartnersResponse)
async def insert_partner(partners_req: PartnersRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = partners.insert().values(dict(partners_req)).returning(ALL_COLUMNS)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='partners Details Inserted failed')
    data = build_partners_post_dict(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(PartnersResponse(**dict(data))))


@partners_router.delete('/{partner_id}', response_model=PartnersResponse)
async def delete_partner(partner_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = partners.select().where(partners.c.id == partner_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No partners Details Found with this ID: {partner_id}')
    else:
        result = partners.delete().where(
            partners.c.id == partner_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'partners Deleted Failed with this ID: {partner_id}')
        data = build_partners_post_dict(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(PartnersResponse(**dict(data))))


@partners_router.put('/{partner_id}', response_model=PartnersResponse)
async def update_partner(partner_id: UUID, partners_req: PartnersRequest, current_user: Login = Depends(get_current_user)):
    result = partners.select().where(partners.c.id == partner_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No partners Details Found with this ID: {partner_id}')
    else:
        result = partners.delete().where(
            partners.c.id == partner_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'partners Deleted Failed with this ID: {partner_id}')
        else:
            result = partners.insert().values(dict(partners_req)).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='partners Details Updated failed')
            data = build_partners_post_dict(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(PartnersResponse(**dict(data))))


@partners_router.patch('/{partner_id}', response_model=PartnersResponse)
async def update(partner_id: UUID, partners_req: PartnersRequest, current_user: Login = Depends(get_current_user)):
    result = partners.select().where(partners.c.id == partner_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No partners Details Found with this ID: {partner_id}')
    else:
        result = partners.update().where(partners.c.id == partner_id).values(
            dict(partners_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='partners Details Updated failed')
        data = build_partners_post_dict(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(PartnersResponse(**dict(data))))
