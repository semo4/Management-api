from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from src.queries.withdraw_contractors import WithdrawContractorsQueries
from src.types.withdraw_contractors import (
    WithdrawContractorsRequest,
    WithdrawContractorsResponse,
)
from src.utils.helper import (
    build_withdraw_contractors_dict,
    build_withdraw_contractors_dict_post,
)

withdraw_contractors_queries = WithdrawContractorsQueries()


class WithdrawContractorsServices:
    def get_withdraw_contractors(self) -> jsonable_encoder:
        withdraw_contractors_list = list()
        result = withdraw_contractors_queries.get_withdraw_contractors()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No withdraw_contractors Details Found",
            )
        for row in result:
            data = build_withdraw_contractors_dict(row)
            withdraw_contractors_list.append(data)
        content = jsonable_encoder(
            WithdrawContractorsResponse(**dict(i)) for i in withdraw_contractors_list
        )
        return content

    def get_operation(self, withdraw_contractors_id: UUID) -> jsonable_encoder:
        row = withdraw_contractors_queries.get_operation(
            withdraw_contractors_id=withdraw_contractors_id
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No withdraw_contractors Details Found with this ID: {withdraw_contractors_id}",
            )
        data = build_withdraw_contractors_dict(row)
        content = jsonable_encoder(WithdrawContractorsResponse(**dict(data)))
        return content

    def get_operation_by_amount(
        self, withdraw_contractors_amount: float
    ) -> jsonable_encoder:
        row = withdraw_contractors_queries.get_operation_by_amount(
            withdraw_contractors_amount=withdraw_contractors_amount
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No withdraw_contractors Details Found with this ID: {withdraw_contractors_amount}",
            )
        data = build_withdraw_contractors_dict(row)
        content = jsonable_encoder(WithdrawContractorsResponse(**dict(data)))
        return content

    def insert_operation(
        self,
        withdraw_contractors_req: WithdrawContractorsRequest,
    ) -> jsonable_encoder:
        row = withdraw_contractors_queries.insert_operation(
            withdraw_contractors_req=withdraw_contractors_req
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="withdraw_contractors Details Inserted failed",
            )
        data = build_withdraw_contractors_dict_post(row)
        content = jsonable_encoder(WithdrawContractorsResponse(**dict(data)))
        return content

    def delete_withdraw_contractors(
        self, withdraw_contractors_id: UUID
    ) -> jsonable_encoder:
        pre_row = withdraw_contractors_queries.get_operation_by_id(
            withdraw_contractors_id=withdraw_contractors_id
        )
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No withdraw_contractors Details Found with this ID: {withdraw_contractors_id}",
            )
        else:
            row = withdraw_contractors_queries.delete_withdraw_contractors(
                withdraw_contractors_id=withdraw_contractors_id
            )

            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"withdraw_contractors Deleted Failed with this ID: {withdraw_contractors_id}",
                )
            data = build_withdraw_contractors_dict_post(row)
            content = jsonable_encoder(WithdrawContractorsResponse(**dict(data)))
            return content

    def update_withdraw_contractors(
        self,
        withdraw_contractors_id: UUID,
        withdraw_contractors_req: WithdrawContractorsRequest,
    ) -> jsonable_encoder:
        row = withdraw_contractors_queries.get_operation_by_id(
            withdraw_contractors_id=withdraw_contractors_id
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No withdraw_contractors Details Found with this ID: {withdraw_contractors_id}",
            )
        else:
            row = withdraw_contractors_queries.delete_withdraw_contractors(
                withdraw_contractors_id=withdraw_contractors_id
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"withdraw_contractors Deleted Failed with this ID: {withdraw_contractors_id}",
                )
            else:
                row = withdraw_contractors_queries.insert_operation(
                    withdraw_contractors_req=withdraw_contractors_req
                )

                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="withdraw_contractors Details Updated failed",
                    )
                data = build_withdraw_contractors_dict_post(row)
                content = jsonable_encoder(WithdrawContractorsResponse(**dict(data)))
                return content

    def update(
        self,
        withdraw_contractors_id: UUID,
        withdraw_contractors_req: WithdrawContractorsRequest,
    ) -> jsonable_encoder:
        row = withdraw_contractors_queries.get_operation_by_id(
            withdraw_contractors_id=withdraw_contractors_id
        )

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No withdraw_contractors Details Found with this ID: {withdraw_contractors_id}",
            )
        else:
            row = withdraw_contractors_queries.update_withdraw_contractors(
                withdraw_contractors_id=withdraw_contractors_id,
                withdraw_contractors_req=withdraw_contractors_req,
            )

            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="withdraw_contractors Details Updated failed",
                )
            data = build_withdraw_contractors_dict_post(row)
            content = jsonable_encoder(WithdrawContractorsResponse(**dict(data)))
            return content
