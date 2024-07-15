from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.oauth2 import get_current_user
from src.services.withdraw_contractors import WithdrawContractorsServices
from src.types.users import Login
from src.types.withdraw_contractors import (
    WithdrawContractorsRequest,
    WithdrawContractorsResponse,
)

withdraw_contractors_router = APIRouter(
    prefix="/withdraw_contractors", tags=["Withdraw Contractors"]
)
withdraw_contractors_services = WithdrawContractorsServices()


@withdraw_contractors_router.get("/", response_model=WithdrawContractorsResponse)
async def get_withdraw_contractors(
    current_user: Login = Depends(get_current_user),
) -> JSONResponse:
    content = withdraw_contractors_services.get_withdraw_contractors()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@withdraw_contractors_router.get(
    "/get_operation/{withdraw_contractors_id}",
    response_model=WithdrawContractorsResponse,
)
async def get_operation(
    withdraw_contractors_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = withdraw_contractors_services.get_operation(
        withdraw_contractors_id=withdraw_contractors_id
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@withdraw_contractors_router.get(
    "/get_operation_by_amount/{withdraw_contractors_amount}",
    response_model=WithdrawContractorsResponse,
)
async def get_operation_by_amount(
    withdraw_contractors_amount: float, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = withdraw_contractors_services.get_operation_by_amount(
        withdraw_contractors_amount=withdraw_contractors_amount
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@withdraw_contractors_router.post("/", response_model=WithdrawContractorsResponse)
async def insert_operation(
    withdraw_contractors_req: WithdrawContractorsRequest,
    current_user: Login = Depends(get_current_user),
) -> JSONResponse:
    content = withdraw_contractors_services.insert_operation(
        withdraw_contractors_req=withdraw_contractors_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@withdraw_contractors_router.delete(
    "/{withdraw_contractors_id}", response_model=WithdrawContractorsResponse
)
async def delete_withdraw_contractors(
    withdraw_contractors_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = withdraw_contractors_services.delete_withdraw_contractors(
        withdraw_contractors_id=withdraw_contractors_id
    )
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@withdraw_contractors_router.put(
    "/{withdraw_contractors_id}", response_model=WithdrawContractorsResponse
)
async def update_withdraw_contractors(
    withdraw_contractors_id: UUID,
    withdraw_contractors_req: WithdrawContractorsRequest,
    current_user: Login = Depends(get_current_user),
):
    content = withdraw_contractors_services.delete_withdraw_contractors(
        withdraw_contractors_id=withdraw_contractors_id,
        withdraw_contractors_req=withdraw_contractors_req,
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@withdraw_contractors_router.patch(
    "/{withdraw_contractors_id}", response_model=WithdrawContractorsResponse
)
async def update(
    withdraw_contractors_id: UUID,
    withdraw_contractors_req: WithdrawContractorsRequest,
    current_user: Login = Depends(get_current_user),
):
    content = withdraw_contractors_services.delete_withdraw_contractors(
        withdraw_contractors_id=withdraw_contractors_id,
        withdraw_contractors_req=withdraw_contractors_req,
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )
