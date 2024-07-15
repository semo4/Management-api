from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.oauth2 import get_current_user
from src.services.projects import ProjectsServices
from src.types.projects import ProjectsRequest, ProjectsResponse
from src.types.users import Login

projects_router = APIRouter(prefix="/projects", tags=["Projects"])

projects_services = ProjectsServices()


@projects_router.get("/", response_model=ProjectsResponse)
async def get_projects(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    content = projects_services.get_projects()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@projects_router.get("/get_project/{project_id}", response_model=ProjectsResponse)
async def get_project(
    project_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = projects_services.get_project(project_id=project_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@projects_router.get(
    "/get_project_by_name/{project_name}", response_model=ProjectsResponse
)
async def get_project_by_name(
    project_name: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = projects_services.get_project_by_name(project_name=project_name)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@projects_router.post("/", response_model=ProjectsResponse)
async def insert_project(
    projects_req: ProjectsRequest, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = projects_services.insert_project(projects_req=projects_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@projects_router.delete("/{project_id}", response_model=ProjectsResponse)
async def delete_project(
    project_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = projects_services.delete_project(project_id=project_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@projects_router.put("/{project_id}", response_model=ProjectsResponse)
async def update_project(
    project_id: UUID,
    projects_req: ProjectsRequest,
    current_user: Login = Depends(get_current_user),
):
    content = projects_services.update_project(
        project_id=project_id, projects_req=projects_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@projects_router.patch("/{project_id}", response_model=ProjectsResponse)
async def update(
    project_id: UUID,
    projects_req: ProjectsRequest,
    current_user: Login = Depends(get_current_user),
):
    content = projects_services.update(project_id=project_id, projects_req=projects_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )
