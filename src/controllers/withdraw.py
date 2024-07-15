from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.oauth2 import get_current_user
from src.services.withdraw import WithdrawServices
from src.types.users import Login
from src.types.withdraw import WithdrawRequest, WithdrawResponse

withdraw_router = APIRouter(prefix="/withdraw", tags=["Withdraw"])

withdraw_services = WithdrawServices()


@withdraw_router.get("/", response_model=WithdrawResponse)
async def get_withdraws(
    current_user: Login = Depends(get_current_user),
) -> JSONResponse:
    content = withdraw_services.get_withdraws()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@withdraw_router.get("/get_withdraw/{withdraw_id}", response_model=WithdrawResponse)
async def get_withdraw(
    withdraw_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = withdraw_services.get_withdraw(withdraw_id=withdraw_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@withdraw_router.get(
    "/get_withdraw_by_amount/{withdraw_amount}", response_model=WithdrawResponse
)
async def get_withdraw_by_amount(
    withdraw_amount: float, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = withdraw_services.get_withdraw_by_amount(withdraw_amount=withdraw_amount)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@withdraw_router.post("/", response_model=WithdrawResponse)
async def insert_withdraw(
    withdraw_req: WithdrawRequest, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = withdraw_services.insert_withdraw(withdraw_req=withdraw_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@withdraw_router.delete("/{withdraw_id}", response_model=WithdrawResponse)
async def delete_withdraw(
    withdraw_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = withdraw_services.delete_withdraw(withdraw_id=withdraw_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@withdraw_router.put("/{withdraw_id}", response_model=WithdrawResponse)
async def update_withdraw(
    withdraw_id: UUID,
    withdraw_req: WithdrawRequest,
    current_user: Login = Depends(get_current_user),
):
    content = withdraw_services.update_withdraw(
        withdraw_id=withdraw_id, withdraw_req=withdraw_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@withdraw_router.patch("/{withdraw_id}", response_model=WithdrawResponse)
async def update(
    withdraw_id: UUID,
    withdraw_req: WithdrawRequest,
    current_user: Login = Depends(get_current_user),
):
    content = withdraw_services.update_withdraw(
        withdraw_id=withdraw_id, withdraw_req=withdraw_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )
