from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.hashpass import Hash
from src.auth.token import create_token
from src.queries.authentication import AuthQueries
from src.types.users import Token, UsersRequest, UsersResponse
from src.utils.generate_token import generate_verify_token
from src.utils.helper import build_users_dict
from src.utils.smtp_server import AccountVerified

query_auth = AuthQueries()
smtp_server = AccountVerified()


# todo the user must send the api name he need to use to get the permission for it as (R,W,U,D)
class AuthServices:
    # todo add role permission to login token
    def login_service(self, request: OAuth2PasswordRequestForm):
        user = self._get_and_validate_user(request.username)
        self._verify_password(user, request.password)
        self._check_user_permissions(user)
        return self._create_token(user.email)

    def _get_and_validate_user(self, email: str):
        user = query_auth.get_login_user_data_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User does not exist with this email: {email}",
            )
        return user

    def _get_validate_user(self, id: str):
        user = query_auth.get_user_data_by_id(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User does not exist with this id: {id}",
            )
        return user

    def _verify_password(self, user, password: str):
        if not Hash.verify(user.password, password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

    # todo add role permission to login token
    def _check_user_permissions(self, user):
        if not user.is_active:
            smtp_server.send_email(user, generate_verify_token())
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is not activated. Please Check Your Email to activate your account to log in.",
            )
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to log in",
            )

    def _create_token(self, email: str):
        access_token = create_token(data={"sub": email})
        return Token(access_token=access_token, token_type="bearer")

    def register_service(self, user_req: UsersRequest) -> dict:
        user = self._create_user(user_req)
        # todo add send email to activate his account
        smtp_server.send_email(user, generate_verify_token())
        return self._format_response(user)

    def _create_user(self, user_req: UsersRequest):
        user = query_auth.register(user_req)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User registration failed",
            )
        return user

    def _activate_user_acount(self, user_req: UsersRequest):
        user = query_auth.activate_user_account(user_req)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User registration failed",
            )
        return user

    def verify_account_service(self, id):
        user = self._get_validate_user(id)
        user.is_active = True
        self._activate_user_acount(user)
        self._format_response(user)

    def _format_response(self, user) -> dict:
        user_data = build_users_dict(user)
        return jsonable_encoder(UsersResponse(**user_data))
