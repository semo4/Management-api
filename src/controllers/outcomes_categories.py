from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.oauth2 import get_current_user
from src.services.outcomes_categories import OutcomesCategoriesServices
from src.types.outcomes_categories import (
    OutcomesCategoriesRequest,
    OutcomesCategoriesResponse,
)
from src.types.users import Login

categories_router = APIRouter(prefix="/categories", tags=["Categories"])

categories_services = OutcomesCategoriesServices()


@categories_router.get("/", response_model=OutcomesCategoriesResponse)
async def get_categories(
    current_user: Login = Depends(get_current_user),
) -> JSONResponse:
    content = categories_services.get_categories()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@categories_router.get(
    "/get_categories/{categories_id}", response_model=OutcomesCategoriesResponse
)
async def get_category(
    categories_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = categories_services.get_category(categories_id=categories_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@categories_router.get(
    "/get_categories_by_title/{categories_title}",
    response_model=OutcomesCategoriesResponse,
)
async def get_categories_by_title(
    categories_title: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = categories_services.get_categories_by_title(
        categories_title=categories_title
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@categories_router.post("/", response_model=OutcomesCategoriesResponse)
async def insert_categories(
    categories_req: OutcomesCategoriesRequest,
    current_user: Login = Depends(get_current_user),
) -> JSONResponse:
    content = categories_services.insert_categories(categories_req=categories_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@categories_router.delete("/{categories_id}", response_model=OutcomesCategoriesResponse)
async def delete_categories(
    categories_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = categories_services.delete_categories(categories_id=categories_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@categories_router.put("/{categories_id}", response_model=OutcomesCategoriesResponse)
async def update_categories(
    categories_id: UUID,
    categories_req: OutcomesCategoriesRequest,
    current_user: Login = Depends(get_current_user),
):
    content = categories_services.update_categories(
        categories_id=categories_id, categories_req=categories_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@categories_router.patch("/{categories_id}", response_model=OutcomesCategoriesResponse)
async def update(
    categories_id: UUID,
    categories_req: OutcomesCategoriesRequest,
    current_user: Login = Depends(get_current_user),
):
    content = categories_services.update(
        categories_id=categories_id, categories_req=categories_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )
