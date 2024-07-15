from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.queries.users import UsersQueries
from src.types.users import (
    UsersRequest,
    UsersRequestIsActive,
    UsersRequestIsAdmin,
    UsersRequestIsStuff,
    UsersResponse,
)
from src.utils.helper import build_users_dict

users_queries = UsersQueries()


class UserServices:
    def get_users(self) -> jsonable_encoder:
        users_list = list()
        result = users_queries.get_users()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No Users Details Found"
            )
        for row in result:
            data = build_users_dict(row)
            users_list.append(data)
        content = jsonable_encoder(UsersResponse(**dict(i)) for i in users_list)
        return content

    def get_user(self, user_id: UUID) -> jsonable_encoder:
        row = users_queries.get_user(user_id=user_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No User Details Found With this ID: {user_id}",
            )

        data = build_users_dict(row)
        content = jsonable_encoder(UsersResponse(**dict(data)))
        return content

    def get_user_by_email(
        self,
        email: str,
    ) -> jsonable_encoder:
        row = users_queries.get_user_by_email(email=email)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No User Details Found With this Email: {email}",
            )

        data = build_users_dict(row)
        content = jsonable_encoder(UsersResponse(**dict(data)))
        return content

    def insert_user(
        self,
        user_req: UsersRequest,
    ) -> jsonable_encoder:
        row = users_queries.insert_user(user_req=user_req)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Users Details Inserted failed",
            )
        data = build_users_dict(row)
        content = jsonable_encoder(UsersResponse(**dict(data)))
        return content

    def delete_user(
        self,
        user_id: UUID,
    ) -> JSONResponse:
        pre_row = users_queries.get_user_by_id(user_id=user_id)
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No User Details Found With this ID: {user_id}",
            )
        else:
            row = users_queries.delete_user(user_id=user_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Deleted Failed with this ID: {user_id}",
                )
            data = build_users_dict(row)
            content = jsonable_encoder(UsersResponse(**dict(data)))
            return content

    def update_user(self, user_id: UUID, user_req: UsersRequest) -> jsonable_encoder:
        row = users_queries.get_user_by_id(user_id=user_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No users Details Found with this ID: {user_id}",
            )
        else:
            row = users_queries.delete_user(user_id=user_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"users Deleted Failed with this ID: {user_id}",
                )
            else:
                row = users_queries.insert_user(user_req=user_req)
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="users Details Updated failed",
                    )
                data = build_users_dict(row)
                content = jsonable_encoder(UsersResponse(**dict(data)))
                return content

    def update(self, user_id: UUID, user_req: UsersRequest) -> jsonable_encoder:
        row = users_queries.get_user_by_id(user_id=user_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No User Details Found with this ID: {user_id}",
            )
        else:
            row = users_queries.update_user(user_id=user_id, user_req=user_req)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="users Details Updated failed",
                )
            data = build_users_dict(row)
            content = jsonable_encoder(UsersResponse(**dict(data)))
            return content

    def update_is_active(
        self, user_id: UUID, user_req: UsersRequestIsActive
    ) -> jsonable_encoder:
        row = users_queries.get_user_by_id(user_id=user_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No User Details Found with this ID: {user_id}",
            )
        else:
            row = users_queries.update_is_active(user_id=user_id, user_req=user_req)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="users Details Updated failed",
                )
            data = build_users_dict(row)
            content = jsonable_encoder(UsersResponse(**dict(data)))
            return content

    def update_is_admin(
        self, user_id: UUID, user_req: UsersRequestIsAdmin
    ) -> jsonable_encoder:
        row = users_queries.get_user_by_id(user_id=user_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No User Details Found with this ID: {user_id}",
            )
        else:
            row = users_queries.update_is_admin(user_id=user_id, user_req=user_req)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="users Details Updated failed",
                )
            data = build_users_dict(row)
            content = jsonable_encoder(UsersResponse(**dict(data)))
            return content

    def update_is_stuff(
        self, user_id: UUID, user_req: UsersRequestIsStuff
    ) -> jsonable_encoder:
        row = users_queries.get_user_by_id(user_id=user_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No User Details Found with this ID: {user_id}",
            )
        else:
            row = users_queries.update_is_stuff(user_id=user_id, user_req=user_req)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="users Details Updated failed",
                )
            data = build_users_dict(row)
            content = jsonable_encoder(UsersResponse(**dict(data)))
            return content
