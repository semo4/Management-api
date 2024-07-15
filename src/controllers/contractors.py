from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.oauth2 import get_current_user
from src.services.contractors import ContractorsServices
from src.types.contractors import ContractorsRequest, ContractorsResponse
from src.types.users import Login

contractors_router = APIRouter(prefix="/contractors", tags=["Contractors"])

contractors_services = ContractorsServices()


@contractors_router.get("/", response_model=ContractorsResponse)
async def get_contractors(
    current_user: Login = Depends(get_current_user),
) -> JSONResponse:
    content = contractors_services.get_contractors()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@contractors_router.get(
    "/get_contractor/{contractor_id}", response_model=ContractorsResponse
)
async def get_contractor(
    contractor_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = contractors_services.get_contractor(contractor_id=contractor_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@contractors_router.get(
    "/get_contractor_by_name/{contractor_name}", response_model=ContractorsResponse
)
async def get_contractor_by_name(
    contractor_name: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = contractors_services.get_contractor_by_name(
        contractor_name=contractor_name
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@contractors_router.post("/", response_model=ContractorsResponse)
async def insert_contractor(
    contractors_req: ContractorsRequest, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = contractors_services.insert_contractor(contractors_req=contractors_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@contractors_router.delete("/{contractor_id}", response_model=ContractorsResponse)
async def delete_contractor(
    contractor_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = contractors_services.delete_contractor(contractor_id=contractor_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@contractors_router.put("/{contractor_id}", response_model=ContractorsResponse)
async def update_contractor(
    contractor_id: UUID,
    contractors_req: ContractorsRequest,
    current_user: Login = Depends(get_current_user),
):
    content = contractors_services.update_contractor(
        contractor_id=contractor_id, contractors_req=contractors_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@contractors_router.patch("/{contractor_id}", response_model=ContractorsResponse)
async def update(
    contractor_id: UUID,
    contractors_req: ContractorsRequest,
    current_user: Login = Depends(get_current_user),
):
    content = contractors_services.update(
        contractor_id=contractor_id, contractors_req=contractors_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )
