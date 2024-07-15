from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.oauth2 import get_current_user
from src.services.sections import SectionsServices
from src.types.sections import SectionsRequest, SectionsResponse
from src.types.users import Login

section_router = APIRouter(prefix="/sections", tags=["Sections"])

section_services = SectionsServices()


@section_router.get("/", response_model=SectionsResponse)
async def get_sections(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    content = section_services.get_sections()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@section_router.get("/get_section/{section_id}", response_model=SectionsResponse)
async def get_section(
    section_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = section_services.get_section(section_id=section_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@section_router.get(
    "/get_section_by_name/{section_name}", response_model=SectionsResponse
)
async def get_section_by_name(
    section_name: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = section_services.get_section_by_name(section_name=section_name)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@section_router.post("/", response_model=SectionsResponse)
async def insert_section(
    section: SectionsRequest, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = section_services.insert_section(section=section)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@section_router.delete("/{section_id}", response_model=SectionsResponse)
async def delete_section(
    section_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = section_services.delete_section(section_id=section_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@section_router.put("/{section_id}", response_model=SectionsResponse)
async def update_section(
    section_id: UUID,
    section: SectionsRequest,
    current_user: Login = Depends(get_current_user),
):
    content = section_services.update_section(section_id=section_id, section=section)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@section_router.patch("/{section_id}", response_model=SectionsResponse)
async def update(
    section_id: UUID,
    section: SectionsRequest,
    current_user: Login = Depends(get_current_user),
):
    content = section_services.update(section_id=section_id, section=section)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )
