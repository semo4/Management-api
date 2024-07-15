from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from src.queries.operations import OperationsQueries
from src.types.operations import OperationsRequest, OperationsResponse
from src.utils.calculation import calculation_operations
from src.utils.helper import build_operations_dict, build_operations_dict_post

operations_queries = OperationsQueries()


class OperationsServices:
    def get_operations(self) -> jsonable_encoder:
        operations_list = list()
        result = operations_queries.get_operations()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No operations Details Found",
            )
        for row in result:
            data = build_operations_dict(row)
            operations_list.append(data)
        content = jsonable_encoder(
            OperationsResponse(**dict(i)) for i in operations_list
        )
        return content

    def get_operation(self, operations_id: UUID) -> jsonable_encoder:
        row = operations_queries.get_operation(operations_id=operations_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No operations Details Found with this ID: {operations_id}",
            )
        data = build_operations_dict(row)
        content = jsonable_encoder(OperationsResponse(**dict(data)))
        return content

    def get_operation_by_working_hours(
        self, operations_working_hours: int
    ) -> jsonable_encoder:
        row = operations_queries.get_operation_by_working_hours(
            operations_working_hours=operations_working_hours
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No operations Details Found with this ID: {operations_working_hours}",
            )
        data = build_operations_dict(row)
        content = jsonable_encoder(OperationsResponse(**dict(data)))
        return content

    def get_operation_by_payment_amount(
        self, operations_payment_amount: float
    ) -> jsonable_encoder:
        row = operations_queries.get_operation_by_payment_amount(
            operations_payment_amount=operations_payment_amount
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No operations Details Found with this ID: {operations_payment_amount}",
            )
        data = build_operations_dict(row)
        content = jsonable_encoder(OperationsResponse(**dict(data)))
        return content

    def insert_operation(self, operations_req: OperationsRequest) -> jsonable_encoder:
        calculated_data = calculation_operations(dict(operations_req))
        if not calculated_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="operations Details Inserted failed",
            )
        row = operations_queries.insert_operation(calculated_data=calculated_data)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="operations Details Inserted failed",
            )
        data = build_operations_dict_post(row)
        content = jsonable_encoder(OperationsResponse(**dict(data)))
        return content

    def delete_operations(self, operations_id: UUID) -> jsonable_encoder:
        pre_row = operations_queries.get_operation_by_id(operations_id=operations_id)
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No operations Details Found with this ID: {operations_id}",
            )
        else:
            row = operations_queries.delete_operations(operations_id=operations_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"operations Deleted Failed with this ID: {operations_id}",
                )
            data = build_operations_dict_post(row)
            content = jsonable_encoder(OperationsResponse(**dict(data)))
            return content

    def update_operations(
        self, operations_id: UUID, operations_req: OperationsRequest
    ) -> jsonable_encoder:
        row = operations_queries.get_operation_by_id(operations_id=operations_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No operations Details Found with this ID: {operations_id}",
            )
        else:
            row = operations_queries.delete_operations(operations_id=operations_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"operations Deleted Failed with this ID: {operations_id}",
                )
            else:
                calculated_data = calculation_operations(dict(operations_req))
                if not calculated_data:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="operations Details Inserted failed",
                    )
                row = operations_queries.insert_operation(
                    calculated_data=calculated_data
                )
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="operations Details Updated failed",
                    )
                data = build_operations_dict_post(row)
                content = jsonable_encoder(OperationsResponse(**dict(data)))
                return content

    def update(
        self,
        operations_id: UUID,
        operations_req: OperationsRequest,
    ) -> jsonable_encoder:
        row = operations_queries.get_operation_by_id(operations_id=operations_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No operations Details Found with this ID: {operations_id}",
            )
        else:
            calculated_data = calculation_operations(
                dict(operations_req.dict(exclude_unset=True))
            )
            if not calculated_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="operations Details Inserted failed",
                )
            row = operations_queries.update_operations(
                operations_id=operations_id, calculated_data=calculated_data
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="operations Details Updated failed",
                )
            data = build_operations_dict_post(row)
            content = jsonable_encoder(OperationsResponse(**dict(data)))
            return content
