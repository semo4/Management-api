from uuid import UUID

from fastapi import APIRouter
from sqlalchemy.sql import select

from src.database.connection import execute_all, execute_one
from src.database.database import ALL_COLUMNS
from src.models.projects import projects
from src.models.sections import sections
from src.types.projects import ProjectsRequest

projects_router = APIRouter(prefix="/projects", tags=["Projects"])


class ProjectsQueries:
    def get_projects(self):
        join_table = projects.join(sections, projects.c.section_id == sections.c.id)
        res = (
            select(
                projects,
                sections.c.name,
            )
            .select_from(join_table)
            .where(projects.c.section_id == sections.c.id)
        )
        result = execute_all(res)
        return result

    def get_project(self, project_id: UUID):
        join_table = projects.join(sections, projects.c.section_id == sections.c.id)
        result = (
            select(projects, sections.c.name)
            .select_from(join_table)
            .where(projects.c.section_id == sections.c.id)
            .where(projects.c.id == project_id)
        )
        row = execute_one(result)
        return row

    def get_project_by_name(self, project_name: str):
        result = (
            select(projects, sections.c.name)
            .select_from(
                projects.join(sections, projects.c.section_id == sections.c.id)
            )
            .where(projects.c.section_id == sections.c.id)
            .where(projects.c.name == project_name)
        )
        row = execute_one(result)
        return row

    def insert_project(self, projects_req: ProjectsRequest):
        result = projects.insert().values(dict(projects_req)).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row

    def get_project_by_id(self, project_id: UUID):
        result = projects.select().where(projects.c.id == project_id)
        row = execute_one(result)
        return row

    def delete_project(self, project_id: UUID):
        result = (
            projects.delete().where(projects.c.id == project_id).returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_project(self, project_id: UUID, projects_req: ProjectsRequest):
        result = (
            projects.update()
            .where(projects.c.id == project_id)
            .values(dict(projects_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row
