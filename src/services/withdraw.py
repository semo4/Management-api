from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from src.queries.withdraw import WithdrawQueries
from src.types.withdraw import WithdrawRequest, WithdrawResponse
from src.utils.helper import build_withdraw_dict, build_withdraw_dict_post

withdraw_queries = WithdrawQueries()


class WithdrawServices:
    def get_withdraws(self) -> jsonable_encoder:
        withdraw_list = list()
        result = withdraw_queries.get_withdraws()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No withdraw Details Found",
            )
        for row in result:
            data = build_withdraw_dict(row)
            withdraw_list.append(data)
        content = jsonable_encoder(WithdrawResponse(**dict(i)) for i in withdraw_list)
        return content

    def get_withdraw(self, withdraw_id: UUID) -> jsonable_encoder:
        row = withdraw_queries.get_withdraw(withdraw_id=withdraw_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No withdraw Details Found with this ID: {withdraw_id}",
            )
        data = build_withdraw_dict(row)
        content = jsonable_encoder(WithdrawResponse(**dict(data)))
        return content

    def get_withdraw_by_amount(self, withdraw_amount: float) -> jsonable_encoder:
        row = withdraw_queries.get_withdraw_by_amount(withdraw_amount=withdraw_amount)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No withdraw Details Found with this ID: {withdraw_amount}",
            )
        data = build_withdraw_dict(row)
        content = jsonable_encoder(WithdrawResponse(**dict(data)))
        return content

    def insert_withdraw(self, withdraw_req: WithdrawRequest) -> jsonable_encoder:
        row = withdraw_queries.insert_withdraw(withdraw_req=withdraw_req)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="withdraw Details Inserted failed",
            )
        data = build_withdraw_dict_post(row)
        content = jsonable_encoder(WithdrawResponse(**dict(data)))
        return content

    def delete_withdraw(self, withdraw_id: UUID) -> jsonable_encoder:
        pre_row = withdraw_queries.get_withdraw_by_id(withdraw_id=withdraw_id)
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No withdraw Details Found with this ID: {withdraw_id}",
            )
        else:
            row = withdraw_queries.delete_withdraw(withdraw_id=withdraw_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"withdraw Deleted Failed with this ID: {withdraw_id}",
                )
            data = build_withdraw_dict_post(row)
            content = jsonable_encoder(WithdrawResponse(**dict(data)))
            return content

    def update_withdraw(
        self, withdraw_id: UUID, withdraw_req: WithdrawRequest
    ) -> jsonable_encoder:
        row = withdraw_queries.get_withdraw_by_id(withdraw_id=withdraw_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No withdraw Details Found with this ID: {withdraw_id}",
            )
        else:
            row = withdraw_queries.delete_withdraw(withdraw_id=withdraw_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"withdraw Deleted Failed with this ID: {withdraw_id}",
                )
            else:
                row = withdraw_queries.insert_withdraw(withdraw_req=withdraw_req)
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="withdraw Details Updated failed",
                    )
                data = build_withdraw_dict_post(row)
                content = jsonable_encoder(WithdrawResponse(**dict(data)))
                return content

    def update(
        self,
        withdraw_id: UUID,
        withdraw_req: WithdrawRequest,
    ):
        row = withdraw_queries.get_withdraw_by_id(withdraw_id=withdraw_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No withdraw Details Found with this ID: {withdraw_id}",
            )
        else:
            row = withdraw_queries.update_withdraw(
                withdraw_id=withdraw_id, withdraw_req=withdraw_req
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="withdraw Details Updated failed",
                )
            data = build_withdraw_dict_post(row)
            content = jsonable_encoder(WithdrawResponse(**dict(data)))
            return content
