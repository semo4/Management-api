from uuid import UUID

from fastapi import APIRouter

from src.auth.hashpass import Hash
from src.database.connection import execute_all, execute_one
from src.database.database import ALL_COLUMNS
from src.models.users import users
from src.types.users import (
    UsersRequest,
    UsersRequestIsActive,
    UsersRequestIsAdmin,
    UsersRequestIsStuff,
)

users_router = APIRouter(prefix="/users", tags=["Users"])


class UsersQueries:
    def get_users(self):
        res = users.select()
        result = execute_all(res)
        return result

    def get_user(self, user_id: UUID):
        res = users.select().where(users.c.id == user_id)
        row = execute_one(res)
        return row

    def get_user_by_email(self, email: str):
        res = users.select().where(users.c.email == email)
        row = execute_one(res)
        return row

    def insert_user(self, user_req: UsersRequest):
        user_req.password = Hash.hashing_pass(user_req.password)
        result = users.insert().values(dict(user_req)).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row

    def get_user_by_id(self, user_id: UUID):
        result = users.select().where(users.c.id == user_id)
        row = execute_one(result)
        return row

    def delete_user(self, user_id: UUID):
        result = users.delete().where(users.c.id == user_id).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row

    def update_user(self, user_id: UUID, user_req: UsersRequest):
        result = (
            users.update()
            .where(users.c.id == user_id)
            .values(dict(user_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_is_active(self, user_id: UUID, user_req: UsersRequestIsActive):
        result = (
            users.update()
            .where(users.c.id == user_id)
            .values(dict(user_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_is_admin(self, user_id: UUID, user_req: UsersRequestIsAdmin):
        result = (
            users.update()
            .where(users.c.id == user_id)
            .values(dict(user_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_is_stuff(self, user_id: UUID, user_req: UsersRequestIsStuff):
        result = (
            users.update()
            .where(users.c.id == user_id)
            .values(dict(user_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row
