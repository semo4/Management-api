from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.models.users import users
from src.types.users import UsersRequest, UsersResponse, UsersRequestIsActive, UsersRequestIsAdmin, UsersRequestIsStuff, Token, Login
from src.database.database import ALL_COLUMNS
from src.database.connection import execute_all, execute_one
from src.utils.helper import build_users_dict
from uuid import UUID
from src.auth.hashpass import Hash
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.token import create_token
from src.auth.oauth2 import get_current_user
users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.get('/', response_model=UsersResponse)
async def get_users(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    users_list = list()
    res = users.select()
    result = execute_all(res)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No Users Details Found')
    for row in result:
        data = build_users_dict(row)
        users_list.append(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(UsersResponse(**dict(i)) for i in users_list))


@users_router.get('/get_user/{user_id}', response_model=UsersResponse)
async def get_user(user_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    res = users.select().where(users.c.id == user_id)
    row = execute_one(res)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No User Details Found With this ID: {user_id}')

    data = build_users_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(UsersResponse(**dict(data))))


@users_router.get('/get_user_by_email/{email}', response_model=UsersResponse)
async def get_user_by_email(email: str, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    res = users.select().where(users.c.email == email)
    row = execute_one(res)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No User Details Found With this Email: {email}')

    data = build_users_dict(row)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(UsersResponse(**dict(data))))


@users_router.post('/', response_model=UsersResponse)
async def insert_user(user_req: UsersRequest, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    user_req.password = Hash.hashing_pass(user_req.password)
    result = users.insert().values(dict(user_req)).returning(ALL_COLUMNS)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Users Details Inserted failed')
    data = build_users_dict(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(UsersResponse(**dict(data))))


@users_router.delete('/{user_id}', response_model=UsersResponse)
async def delete_user(user_id: UUID, current_user: Login = Depends(get_current_user)) -> JSONResponse:
    result = users.select().where(users.c.id == user_id)
    pre_row = execute_one(result)
    if not pre_row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'No User Details Found With this ID: {user_id}')
    else:
        result = users.delete().where(users.c.id == user_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Deleted Failed with this ID: {user_id}')
        data = build_users_dict(row)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content=jsonable_encoder(UsersResponse(**dict(data))))


@users_router.put('/{user_id}', response_model=UsersResponse)
async def update_user(user_id: UUID, user_req: UsersRequest, current_user: Login = Depends(get_current_user)):
    result = users.select().where(users.c.id == user_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No users Details Found with this ID: {user_id}')
    else:
        result = users.delete().where(
            users.c.id == user_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'users Deleted Failed with this ID: {user_id}')
        else:
            result = users.insert().values(dict(user_req)).returning(ALL_COLUMNS)
            row = execute_one(result)
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='users Details Updated failed')
            data = build_users_dict(row)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(UsersResponse(**dict(data))))


@users_router.patch('/{user_id}', response_model=UsersResponse)
async def update(user_id: UUID, user_req: UsersRequest, current_user: Login = Depends(get_current_user)):
    result = users.select().where(users.c.id == user_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No User Details Found with this ID: {user_id}')
    else:
        result = users.update().where(users.c.id == user_id).values(
            dict(user_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='users Details Updated failed')
        data = build_users_dict(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(UsersResponse(**dict(data))))


@users_router.patch('/user_active/{user_id}', response_model=UsersResponse)
async def update_is_active(user_id: UUID, user_req: UsersRequestIsActive, current_user: Login = Depends(get_current_user)):
    result = users.select().where(users.c.id == user_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No User Details Found with this ID: {user_id}')
    else:
        result = users.update().where(users.c.id == user_id).values(
            dict(user_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='users Details Updated failed')
        data = build_users_dict(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(UsersResponse(**dict(data))))


@users_router.patch('/user_admin/{user_id}', response_model=UsersResponse)
async def update_is_admin(user_id: UUID, user_req: UsersRequestIsAdmin, current_user: Login = Depends(get_current_user)):
    result = users.select().where(users.c.id == user_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No User Details Found with this ID: {user_id}')
    else:
        result = users.update().where(users.c.id == user_id).values(
            dict(user_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='users Details Updated failed')
        data = build_users_dict(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(UsersResponse(**dict(data))))


@users_router.patch('/user_stuff/{user_id}', response_model=UsersResponse)
async def update_is_stuff(user_id: UUID, user_req: UsersRequestIsStuff, current_user: Login = Depends(get_current_user)):
    result = users.select().where(users.c.id == user_id)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No User Details Found with this ID: {user_id}')
    else:
        result = users.update().where(users.c.id == user_id).values(
            dict(user_req.dict(exclude_unset=True))).returning(ALL_COLUMNS)
        row = execute_one(result)
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='users Details Updated failed')
        data = build_users_dict(row)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(UsersResponse(**dict(data))))


@users_router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends()):
    result = users.select().where(users.c.email == request.username)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No User Details Found with this Email: {request.username}')
    if not Hash.verify(result.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Incorrect username or password')
    if not result.is_active and result.is_admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="You Don't have permission to log in")
    access_token = create_token(data={"sub": result.email})
    return Token(access_token=access_token, token_type='bearer')


@users_router.post('/register', response_model=UsersResponse)
async def register(user_req: UsersRequest) -> JSONResponse:
    user_req.password = Hash.hashing_pass(user_req.password)
    user_req.is_admin = True
    user_req.is_active = True
    result = users.insert().values(dict(user_req)).returning(ALL_COLUMNS)
    row = execute_one(result)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Users Details Inserted failed')
    data = build_users_dict(row)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(UsersResponse(**dict(data))))
