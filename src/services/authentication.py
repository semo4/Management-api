from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.hashpass import Hash
from src.auth.token import create_token
from src.queries.authentication import AuthQueries
from src.types.users import Token, UsersRequest, UsersResponse
from src.utils.helper import build_users_dict

query_auth = AuthQueries()


class AuthServices:
    # todo add role permission to login token
    def login_service(self, request: OAuth2PasswordRequestForm):
        row = query_auth.get_login_user_data_by_email(request.username)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User Not Exist with this Email: {request.username}",
            )
        if not Hash.verify(row.password, request.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username or password",
            )
        if not row.is_active:
            # todo add smtp server to send activation code
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You Don't Activate your Account permission to log in",
            )
        if not row.is_admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You Don't have permission to LogIn",
            )
        access_token = create_token(data={"sub": row.email})
        return Token(access_token=access_token, token_type="bearer")

    def register_service(self, user_req: UsersRequest) -> jsonable_encoder:
        row = query_auth.register(user_req)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Users Details Inserted failed",
            )
        data = build_users_dict(row)
        return jsonable_encoder(UsersResponse(**dict(data)))
