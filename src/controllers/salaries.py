from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.oauth2 import get_current_user
from src.services.salaries import SalariesServices
from src.types.salaries import SalariesRequest, SalariesResponse
from src.types.users import Login

salaries_router = APIRouter(prefix="/salaries", tags=["Salaries"])


salaries_services = SalariesServices()


@salaries_router.get("/", response_model=SalariesResponse)
async def get_salaries(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    content = salaries_services.get_salaries()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@salaries_router.get("/get_salary/{salaries_id}", response_model=SalariesResponse)
async def get_salary(
    salaries_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = salaries_services.get_salary(salaries_id=salaries_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@salaries_router.get(
    "/get_salary_by_salary_type/{salary_type}", response_model=SalariesResponse
)
async def get_salary_by_salary_type(
    salary_type: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = salaries_services.get_salary_by_salary_type(salary_type=salary_type)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@salaries_router.post("/", response_model=SalariesResponse)
async def insert_salary(
    salaries_req: SalariesRequest, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = salaries_services.insert_salary(salaries_req=salaries_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@salaries_router.delete("/{salaries_id}", response_model=SalariesResponse)
async def delete_salary(
    salaries_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = salaries_services.delete_salary(salaries_id=salaries_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@salaries_router.put("/{salaries_id}", response_model=SalariesResponse)
async def update_salary(
    salaries_id: UUID,
    salaries_req: SalariesRequest,
    current_user: Login = Depends(get_current_user),
):
    content = salaries_services.update_salary(
        salaries_id=salaries_id, salaries_req=salaries_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@salaries_router.patch("/{salaries_id}", response_model=SalariesResponse)
async def update(
    salaries_id: UUID,
    salaries_req: SalariesRequest,
    current_user: Login = Depends(get_current_user),
):
    content = salaries_services.update(
        salaries_id=salaries_id, salaries_req=salaries_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )
