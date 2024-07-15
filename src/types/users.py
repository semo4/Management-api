from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UsersResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    is_super_admin: Optional[bool] = False
    is_admin: Optional[bool] = False
    is_active: Optional[bool] = False
    is_stuff: Optional[bool] = False


class UsersRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    is_super_admin: Optional[bool] = False
    is_admin: Optional[bool] = False
    is_active: Optional[bool] = False
    is_stuff: Optional[bool] = False


class UsersRequestIsAdmin(BaseModel):
    is_admin: bool


class UsersRequestIsActive(BaseModel):
    is_active: bool


class UsersRequestIsStuff(BaseModel):
    is_stuff: bool


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
