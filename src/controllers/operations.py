from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.oauth2 import get_current_user
from src.services.operations import OperationsServices
from src.types.operations import OperationsRequest, OperationsResponse
from src.types.users import Login

operations_router = APIRouter(prefix="/operations", tags=["Operations"])
operations_services = OperationsServices()


@operations_router.get("/", response_model=OperationsResponse)
async def get_operations(
    current_user: Login = Depends(get_current_user),
) -> JSONResponse:
    content = operations_services.get_operations()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@operations_router.get(
    "/get_operation/{operations_id}", response_model=OperationsResponse
)
async def get_operation(
    operations_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = operations_services.get_operation(operations_id=operations_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@operations_router.get(
    "/get_operation_by_working_hours/{operations_working_hours}",
    response_model=OperationsResponse,
)
async def get_operation_by_working_hours(
    operations_working_hours: int, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = operations_services.get_operation_by_working_hours(
        operations_working_hours=operations_working_hours
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@operations_router.get(
    "/get_operation_by_payment_amount/{operations_payment_amount}",
    response_model=OperationsResponse,
)
async def get_operation_by_payment_amount(
    operations_payment_amount: float, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = operations_services.get_operation_by_payment_amount(
        operations_payment_amount=operations_payment_amount
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@operations_router.post("/", response_model=OperationsResponse)
async def insert_operation(
    operations_req: OperationsRequest, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = operations_services.insert_operation(operations_req=operations_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@operations_router.delete("/{operations_id}", response_model=OperationsResponse)
async def delete_operations(
    operations_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = operations_services.delete_operations(operations_id=operations_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@operations_router.put("/{operations_id}", response_model=OperationsResponse)
async def update_operations(
    operations_id: UUID,
    operations_req: OperationsRequest,
    current_user: Login = Depends(get_current_user),
):
    content = operations_services.update_operations(
        operations_id=operations_id, operations_req=operations_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@operations_router.patch("/{operations_id}", response_model=OperationsResponse)
async def update(
    operations_id: UUID,
    operations_req: OperationsRequest,
    current_user: Login = Depends(get_current_user),
):
    content = operations_services.update(
        operations_id=operations_id, operations_req=operations_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )
