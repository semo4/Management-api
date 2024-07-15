from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.services.authentication import AuthServices
from src.types.users import UsersRequest, UsersResponse

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

auth_services = AuthServices()


@auth_router.post("/")
async def login(request: OAuth2PasswordRequestForm = Depends()):
    token_result = auth_services.login_service(request)
    return token_result


@auth_router.post("/register", response_model=UsersResponse)
async def register(user_req: UsersRequest) -> JSONResponse:
    result = auth_services.register_service(user_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=result,
    )
