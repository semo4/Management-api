from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.oauth2 import get_current_user
from src.services.partners import PartnersServices
from src.types.partners import PartnersRequest, PartnersResponse
from src.types.users import Login

partners_router = APIRouter(prefix="/partners", tags=["Partners"])

partners_services = PartnersServices()


@partners_router.get("/", response_model=PartnersResponse)
async def get_partners(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    content = partners_services.get_partners()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@partners_router.get("/get_partner/{partner_id}", response_model=PartnersResponse)
async def get_partner(
    partner_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = partners_services.get_partner(partner_id=partner_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@partners_router.get(
    "/get_partner_by_name/{partner_name}", response_model=PartnersResponse
)
async def get_partner_by_name(
    partner_name: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = partners_services.get_partner_by_name(partner_name=partner_name)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@partners_router.post("/", response_model=PartnersResponse)
async def insert_partner(
    partners_req: PartnersRequest, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = partners_services.insert_partner(partners_req=partners_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@partners_router.delete("/{partner_id}", response_model=PartnersResponse)
async def delete_partner(
    partner_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = partners_services.delete_partner(partner_id=partner_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@partners_router.put("/{partner_id}", response_model=PartnersResponse)
async def update_partner(
    partner_id: UUID,
    partners_req: PartnersRequest,
    current_user: Login = Depends(get_current_user),
):
    content = partners_services.update_partner(
        partner_id=partner_id, partners_req=partners_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@partners_router.patch("/{partner_id}", response_model=PartnersResponse)
async def update(
    partner_id: UUID,
    partners_req: PartnersRequest,
    current_user: Login = Depends(get_current_user),
):
    content = partners_services.update(partner_id=partner_id, partners_req=partners_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )
