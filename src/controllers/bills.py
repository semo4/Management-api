from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.oauth2 import get_current_user
from src.services.bills import BillsServices
from src.types.bills import BillsRequest, BillsResponse
from src.types.users import Login

bills_router = APIRouter(prefix="/bills", tags=["Bills"])

bills_services = BillsServices()


@bills_router.get("/", response_model=BillsResponse)
async def get_bills(
    current_user: Login = Depends(get_current_user),
) -> JSONResponse:
    content = bills_services.get_bills()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@bills_router.get("/get_bill/{bill_id}", response_model=BillsResponse)
async def get_bill(
    bill_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = bills_services.get_bill()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@bills_router.get(
    "/get_bill_by_store_name/{bill_store_name}", response_model=BillsResponse
)
async def get_bill_by_name(
    bill_store_name: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = bills_services.get_bill_by_name(bill_store_name=bill_store_name)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@bills_router.get(
    "/get_bill_by_buyer_name/{bill_buyer_name}", response_model=BillsResponse
)
async def get_bill_by_buyer_name(
    bill_buyer_name: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = bills_services.get_bill_by_buyer_name(bill_buyer_name=bill_buyer_name)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@bills_router.get(
    "/get_bill_by_bill_number/{bill_number}", response_model=BillsResponse
)
async def get_bill_by_bill_number(
    bill_number: int, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = bills_services.get_bill_by_bill_number(bill_number=bill_number)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@bills_router.post("/", response_model=BillsResponse)
async def insert_bill(
    bills_req: BillsRequest, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = bills_services.insert_bill(bills_req=bills_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@bills_router.delete("/{bill_id}", response_model=BillsResponse)
async def delete_bill(
    bill_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = bills_services.delete_bill(bill_id=bill_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@bills_router.put("/{bill_id}", response_model=BillsResponse)
async def update_bill(
    bill_id: UUID,
    bills_req: BillsRequest,
    current_user: Login = Depends(get_current_user),
):
    content = bills_services.update_bill(bill_id=bill_id, bills_req=bills_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@bills_router.patch("/{bill_id}", response_model=BillsResponse)
async def update(
    bill_id: UUID,
    bills_req: BillsRequest,
    current_user: Login = Depends(get_current_user),
):
    content = bills_services.update(bill_id=bill_id, bills_req=bills_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )
