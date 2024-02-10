from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.database.database import ALL_COLUMNS
from uuid import UUID
from src.models.sections import sections
from src.types.sections import SectionsRequest, SectionsResponse
from src.database.connection import execute_all, execute_one
from src.utils.helper import build_section_dict
from src.auth.oauth2 import get_current_user
from src.types.users import Login


section_router = APIRouter(prefix='/sections', tags=['Sections'])


@section_router.get('/', response_model=SectionsResponse)
async def get_sections(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    sections_list = list()
    result = execute_all(sections.select())
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No sections Details Found')
    for row in result:
        data = build_section_dict(row)
        sections_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(SectionsResponse(**dict(i)) for i in sections_list))


@section_router.get('/get_section/{section_id}', response_model=SectionsResponse)
async def get_section(section_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = sections.select().where(sections.c.id == section_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No section Details Found with this ID: {section_id}')
    data = build_section_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(SectionsResponse(**dict(data))))


@section_router.get('/get_section_by_name/{section_name}', response_model=SectionsResponse)
async def get_section_by_name(section_name: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = sections.select().where(sections.c.name == section_name)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No section Details Found with this Name: {section_name}')
    data = build_section_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(SectionsResponse(**dict(data))))


@section_router.post('/', response_model=SectionsResponse)
async def insert_section(section: SectionsRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = sections.insert().values(dict(section)).returning(ALL_COLUMNS)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='section Details Inserted failed')
    data = build_section_dict(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(SectionsResponse(**dict(data))))


@section_router.delete('/{section_id}', response_model=SectionsResponse)
async def delete_section(section_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = sections.select().where(sections.c.id == section_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No section Details Found with this ID: {section_id}')
    else:
        result = sections.delete().where(sections.c.id == section_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'section Deleted Failed with this ID: {section_id}')
        data = build_section_dict(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(SectionsResponse(**dict(data))))


@section_router.put('/{section_id}', response_model=SectionsResponse)
async def update_section(section_id: UUID, section: SectionsRequest, current_user: Login = Depends(get_current_user)):
    result = sections.select().where(sections.c.id == section_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No section Details Found with this ID: {section_id}')
    else:
        result = sections.delete().where(sections.c.id == section_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'section Deleted Failed with this ID: {section_id}')
        else:
            result = sections.insert().values(dict(section)).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='section Details Updated failed')
            data = build_section_dict(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(SectionsResponse(**dict(data))))


@section_router.patch('/{section_id}', response_model=SectionsResponse)
async def update(section_id: UUID, section: SectionsRequest, current_user: Login = Depends(get_current_user)):
    result = sections.select().where(sections.c.id == section_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No section Details Found with this ID: {section_id}')
    else:
        result = sections.update().where(sections.c.id == section_id).values(
            dict(section.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='section Details Updated failed')
        data = build_section_dict(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(SectionsResponse(**dict(data))))
