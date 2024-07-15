from typing import Literal

from sqlalchemy.engine import Row

from src.auth.hashpass import Hash
from src.database.connection import execute_one
from src.database.database import ALL_COLUMNS
from src.models.users import users
from src.types.users import UsersRequest


class AuthQueries:
    def get_login_user_data_by_email(self, email: str) -> Row | Literal[False]:
        result = users.select().where(users.c.email == email)
        row = execute_one(result)
        return row

    def get_login_user_data_by_username(self, username: str) -> Row | Literal[False]:
        result = users.select().where(users.c.username == username)
        row = execute_one(result)
        return row

    def register(self, user_req: UsersRequest) -> Row | Literal[False]:
        user_req.password = Hash.hashing_pass(user_req.password)
        user_req.is_admin = False
        user_req.is_active = False
        user_req.is_super_admin = False
        result = users.insert().values(dict(user_req)).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row
