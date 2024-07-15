from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.oauth2 import get_current_user
from src.services.users import UserServices
from src.types.users import (
    Login,
    UsersRequest,
    UsersRequestIsActive,
    UsersRequestIsAdmin,
    UsersRequestIsStuff,
    UsersResponse,
)

users_router = APIRouter(prefix="/users", tags=["Users"])

users_services = UserServices()


@users_router.get("/", response_model=UsersResponse)
async def get_users(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    content = users_services.get_users()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@users_router.get("/get_user/{user_id}", response_model=UsersResponse)
async def get_user(
    user_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = users_services.get_user(user_id=user_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@users_router.get("/get_user_by_email/{email}", response_model=UsersResponse)
async def get_user_by_email(
    email: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = users_services.get_user_by_email(email=email)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@users_router.post("/", response_model=UsersResponse)
async def insert_user(
    user_req: UsersRequest, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = users_services.insert_user(user_req=user_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@users_router.delete("/{user_id}", response_model=UsersResponse)
async def delete_user(
    user_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = users_services.delete_user(user_id=user_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@users_router.put("/{user_id}", response_model=UsersResponse)
async def update_user(
    user_id: UUID,
    user_req: UsersRequest,
    current_user: Login = Depends(get_current_user),
):
    content = users_services.update_user(user_id=user_id, user_req=user_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@users_router.patch("/{user_id}", response_model=UsersResponse)
async def update(
    user_id: UUID,
    user_req: UsersRequest,
    current_user: Login = Depends(get_current_user),
):
    content = users_services.update(user_id=user_id, user_req=user_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@users_router.patch("/user_active/{user_id}", response_model=UsersResponse)
async def update_is_active(
    user_id: UUID,
    user_req: UsersRequestIsActive,
    current_user: Login = Depends(get_current_user),
):
    content = users_services.update_is_active(user_id=user_id, user_req=user_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@users_router.patch("/user_admin/{user_id}", response_model=UsersResponse)
async def update_is_admin(
    user_id: UUID,
    user_req: UsersRequestIsAdmin,
    current_user: Login = Depends(get_current_user),
):
    content = users_services.update_is_admin(user_id=user_id, user_req=user_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@users_router.patch("/user_stuff/{user_id}", response_model=UsersResponse)
async def update_is_stuff(
    user_id: UUID,
    user_req: UsersRequestIsStuff,
    current_user: Login = Depends(get_current_user),
):
    content = users_services.update_is_stuff(user_id=user_id, user_req=user_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )
