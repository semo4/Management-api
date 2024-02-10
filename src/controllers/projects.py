from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.database.database import ALL_COLUMNS
from uuid import UUID
from src.models.projects import projects
from src.models.sections import sections
from src.types.projects import ProjectsRequest, ProjectsResponse
from src.database.connection import execute_all, execute_one
from src.utils.helper import build_projects_dict, build_projects_post_dict
from sqlalchemy.sql import select
from src.auth.oauth2 import get_current_user
from src.types.users import Login


projects_router = APIRouter(prefix='/projects', tags=['Projects'])


@projects_router.get('/', response_model=ProjectsResponse)
async def get_projects(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    projects_list = list()
    join_table = projects.join(
        sections, projects.c.section_id == sections.c.id)
    res = select(projects, sections.c.name).select_from(
        join_table).where(projects.c.section_id == sections.c.id)
    result = execute_all(res)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No projects Details Found')
    for row in result:
        data = build_projects_dict(row)
        projects_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(ProjectsResponse(**dict(i)) for i in projects_list))


@projects_router.get('/get_project/{project_id}', response_model=ProjectsResponse)
async def get_project(project_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    join_table = projects.join(
        sections, projects.c.section_id == sections.c.id)
    result = select(projects, sections.c.name).select_from(join_table).where(
        projects.c.section_id == sections.c.id).where(projects.c.id == project_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No projects Details Found with this ID: {project_id}')
    data = build_projects_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(ProjectsResponse(**dict(data))))


@projects_router.get('/get_project_by_name/{project_name}', response_model=ProjectsResponse)
async def get_project_by_name(project_name: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = select(projects, sections.c.name).select_from(
        projects.join(sections, projects.c.section_id == sections.c.id)).where(
            projects.c.section_id == sections.c.id).where(projects.c.name == project_name)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No projects Details Found with this Name: {project_name}')
    data = build_projects_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(ProjectsResponse(**dict(data))))


@projects_router.post('/', response_model=ProjectsResponse)
async def insert_project(projects_req: ProjectsRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = projects.insert().values(dict(projects_req)).returning(ALL_COLUMNS)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='projects Details Inserted failed')
    data = build_projects_post_dict(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(ProjectsResponse(**dict(data))))


@projects_router.delete('/{project_id}', response_model=ProjectsResponse)
async def delete_project(project_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = projects.select().where(projects.c.id == project_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No projects Details Found with this ID: {project_id}')
    else:
        result = projects.delete().where(
            projects.c.id == project_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'projects Deleted Failed with this ID: {project_id}')
        data = build_projects_post_dict(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(ProjectsResponse(**dict(data))))


@projects_router.put('/{project_id}', response_model=ProjectsResponse)
async def update_project(project_id: UUID, projects_req: ProjectsRequest, current_user: Login = Depends(get_current_user)):
    result = projects.select().where(projects.c.id == project_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No projects Details Found with this ID: {project_id}')
    else:
        result = projects.delete().where(
            projects.c.id == project_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'projects Deleted Failed with this ID: {project_id}')
        else:
            result = projects.insert().values(dict(projects_req)).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='projects Details Updated failed')
            data = build_projects_post_dict(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(ProjectsResponse(**dict(data))))


@projects_router.patch('/{project_id}', response_model=ProjectsResponse)
async def update(project_id: UUID, projects_req: ProjectsRequest, current_user: Login = Depends(get_current_user)):
    result = projects.select().where(projects.c.id == project_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No projects Details Found with this ID: {project_id}')
    else:
        result = projects.update().where(projects.c.id == project_id).values(
            dict(projects_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='projects Details Updated failed')
        data = build_projects_post_dict(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(ProjectsResponse(**dict(data))))
