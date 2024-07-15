from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.oauth2 import get_current_user
from src.services.workplaces import WorkPlaceServices
from src.types.users import Login
from src.types.workplaces import WorkPlacesRequest, WorkPlacesResponse

workplace_router = APIRouter(prefix="/workplace", tags=["WorkPlace"])

workplace_services = WorkPlaceServices()


@workplace_router.get("/", response_model=WorkPlacesResponse)
async def get_workplaces(
    current_user: Login = Depends(get_current_user),
) -> JSONResponse:
    content = workplace_services.get_workplaces()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@workplace_router.get(
    "/get_workplace/{workplace_id}", response_model=WorkPlacesResponse
)
async def get_workplace(
    workplace_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = workplace_services.get_workplace(workplace_id=workplace_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@workplace_router.get(
    "/get_workplace_by_title/{workplace_title}", response_model=WorkPlacesResponse
)
async def get_workplace_by_title(
    workplace_title: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = workplace_services.get_workplace_by_title(workplace_title=workplace_title)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@workplace_router.post("/", response_model=WorkPlacesResponse)
async def insert_workplace(
    workplace_req: WorkPlacesRequest, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = workplace_services.insert_workplace(workplace_req=workplace_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@workplace_router.delete("/{workplace_id}", response_model=WorkPlacesResponse)
async def delete_workplace(
    workplace_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = workplace_services.delete_workplace(workplace_id=workplace_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@workplace_router.put("/{workplace_id}", response_model=WorkPlacesResponse)
async def update_workplace(
    workplace_id: UUID,
    workplace_req: WorkPlacesRequest,
    current_user: Login = Depends(get_current_user),
):
    content = workplace_services.update_workplace(
        workplace_id=workplace_id, workplace_req=workplace_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@workplace_router.patch("/{workplace_id}", response_model=WorkPlacesResponse)
async def update(
    workplace_id: UUID,
    workplace_req: WorkPlacesRequest,
    current_user: Login = Depends(get_current_user),
):
    content = workplace_services.update(
        workplace_id=workplace_id, workplace_req=workplace_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )
