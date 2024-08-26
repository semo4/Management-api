from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder

from src.queries.projects import ProjectsQueries
from src.types.projects import ProjectsRequest, ProjectsResponse
from src.utils.helper import build_projects_dict, build_projects_post_dict

projects_router = APIRouter(prefix="/projects", tags=["Projects"])

projects_queries = ProjectsQueries()


class ProjectsServices:
    def get_projects(self) -> jsonable_encoder:
        projects_list = list()
        result = projects_queries.get_projects()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No projects Details Found",
            )
        for row in result:
            data = build_projects_dict(row)
            projects_list.append(ProjectsResponse(**dict(data)))
        content = jsonable_encoder(projects_list)
        return content

    def get_project(self, project_id: UUID) -> jsonable_encoder:
        row = projects_queries.get_project(project_id=project_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No projects Details Found with this ID: {project_id}",
            )
        data = build_projects_dict(row)
        content = jsonable_encoder(ProjectsResponse(**dict(data)))
        return content

    def get_project_by_name(self, project_name: str) -> jsonable_encoder:
        row = projects_queries.get_project_by_name(project_name=project_name)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No projects Details Found with this Name: {project_name}",
            )
        data = build_projects_dict(row)
        content = jsonable_encoder(ProjectsResponse(**dict(data)))
        return content

    def insert_project(self, projects_req: ProjectsRequest) -> jsonable_encoder:
        row = projects_queries.insert_project(projects_req=projects_req)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="projects Details Inserted failed",
            )
        data = build_projects_post_dict(row)
        content = jsonable_encoder(ProjectsResponse(**dict(data)))
        return content

    def delete_project(self, project_id: UUID) -> jsonable_encoder:
        pre_row = projects_queries.get_project_by_id(project_id=project_id)
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No projects Details Found with this ID: {project_id}",
            )
        else:
            row = projects_queries.delete_project(project_id=project_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"projects Deleted Failed with this ID: {project_id}",
                )
            data = build_projects_post_dict(row)
            content = jsonable_encoder(ProjectsResponse(**dict(data)))
            return content

    def update_project(
        self, project_id: UUID, projects_req: ProjectsRequest
    ) -> jsonable_encoder:
        row = projects_queries.get_project_by_id(project_id=project_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No projects Details Found with this ID: {project_id}",
            )
        else:
            row = projects_queries.delete_project(project_id=project_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"projects Deleted Failed with this ID: {project_id}",
                )
            else:
                row = projects_queries.insert_project(projects_req=projects_req)
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="projects Details Updated failed",
                    )
                data = build_projects_post_dict(row)
                content = jsonable_encoder(ProjectsResponse(**dict(data)))
                return content

    def update(
        self, project_id: UUID, projects_req: ProjectsRequest
    ) -> jsonable_encoder:
        row = projects_queries.get_project_by_id(project_id=project_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No projects Details Found with this ID: {project_id}",
            )
        else:
            row = projects_queries.update_project(
                project_id=project_id, projects_req=projects_req
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="projects Details Updated failed",
                )
            data = build_projects_post_dict(row)
            content = jsonable_encoder(ProjectsResponse(**dict(data)))
            return content
