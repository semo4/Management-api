from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.oauth2 import get_current_user
from src.services.incomes import IncomesServices
from src.types.incomes import IncomesRequest, IncomesResponse
from src.types.users import Login

incomes_router = APIRouter(prefix="/incomes", tags=["Incomes"])

incomes_services = IncomesServices()


@incomes_router.get("/", response_model=IncomesResponse)
async def get_incomes(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    content = incomes_services.get_incomes()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@incomes_router.get("/get_income/{income_id}", response_model=IncomesResponse)
async def get_income(
    income_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = incomes_services.get_income(income_id=income_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@incomes_router.get(
    "/get_income_by_receiving_person/{income_receiving_person}",
    response_model=IncomesResponse,
)
async def get_income_by_receiving_person(
    income_receiving_person: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = incomes_services.get_income_by_receiving_person(
        income_receiving_person=income_receiving_person
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@incomes_router.get(
    "/get_income_by_gave_person/{income_gave_person}", response_model=IncomesResponse
)
async def get_income_by_gave_person(
    income_gave_person: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = incomes_services.get_income_by_gave_person(
        income_gave_person=income_gave_person
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@incomes_router.get(
    "/get_income_by_check_number/{income_check_number}", response_model=IncomesResponse
)
async def get_income_by_check_number(
    income_check_number: int, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = incomes_services.get_income_by_check_number(
        income_check_number=income_check_number
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@incomes_router.get(
    "/get_income_by_way_of_receiving/{income_way_of_receiving}",
    response_model=IncomesResponse,
)
async def get_income_by_way_of_receiving(
    income_way_of_receiving: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = incomes_services.get_income_by_way_of_receiving(
        income_way_of_receiving=income_way_of_receiving
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@incomes_router.post("/", response_model=IncomesResponse)
async def insert_income(
    incomes_req: IncomesRequest, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = incomes_services.insert_income(incomes_req=incomes_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@incomes_router.delete("/{income_id}", response_model=IncomesResponse)
async def delete_income(
    income_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = incomes_services.delete_income(income_id=income_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@incomes_router.put("/{income_id}", response_model=IncomesResponse)
async def update_income(
    income_id: UUID,
    incomes_req: IncomesRequest,
    current_user: Login = Depends(get_current_user),
):
    content = incomes_services.update_income(
        income_id=income_id, incomes_req=incomes_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@incomes_router.patch("/{income_id}", response_model=IncomesResponse)
async def update(
    income_id: UUID,
    incomes_req: IncomesRequest,
    current_user: Login = Depends(get_current_user),
):
    content = incomes_services.update(income_id=income_id, incomes_req=incomes_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )
