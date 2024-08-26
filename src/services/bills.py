from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from src.queries.bills import BillsQueries
from src.types.bills import BillsRequest, BillsResponse
from src.utils.helper import build_bills_dict, build_bills_post_dict

bills_query = BillsQueries()


class BillsServices:
    def get_bills(self) -> List[dict]:
        result = bills_query.get_bills()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No bills found"
            )

        try:
            bills_list = [BillsResponse(**build_bills_dict(row)) for row in result]
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing bill data",
            ) from e

        return jsonable_encoder(bills_list)

    def get_bill(self, bill_id: UUID) -> dict:
        row = bills_query.get_bill(bill_id=bill_id)

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found"
            )

        try:
            bill_data = build_bills_dict(row)
            bill = BillsResponse(**bill_data)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing bill data",
            ) from e

        return jsonable_encoder(bill)

    def get_bill_by_name(self, bill_store_name: str) -> dict:
        row = bills_query.get_bill_by_name(bill_store_name=bill_store_name)

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found"
            )

        try:
            bill_data = build_bills_dict(row)
            bill = BillsResponse(**bill_data)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing bill data",
            ) from e

        return jsonable_encoder(bill)

    def get_bill_by_buyer_name(self, bill_buyer_name: str) -> dict:
        row = bills_query.get_bill_by_buyer_name(bill_buyer_name=bill_buyer_name)

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No bills found for the specified buyer",
            )

        try:
            bill_data = build_bills_dict(row)
            bill = BillsResponse(**bill_data)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing bill data",
            ) from e

        return jsonable_encoder(bill)

    def get_bill_by_bill_number(self, bill_number: int) -> dict:
        row = bills_query.get_bill_by_bill_number(bill_number=bill_number)

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found"
            )

        try:
            bill_data = build_bills_dict(row)
            bill = BillsResponse(**bill_data)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing bill data",
            ) from e

        return jsonable_encoder(bill)

    def insert_bill(self, bills_req: BillsRequest) -> dict:
        try:
            row = bills_query.insert_bill(bills_req=bills_req)

            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to insert bill details",
                )

            bill_data = build_bills_post_dict(row)
            bill = BillsResponse(**bill_data)

            return jsonable_encoder(bill)

        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid bill data format",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request",
            ) from e

    def delete_bill(self, bill_id: UUID) -> dict:
        try:
            # Check if the bill exists
            if not bills_query.get_bill_by_id(bill_id=bill_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found"
                )

            # Attempt to delete the bill
            deleted_row = bills_query.delete_bill(bill_id)

            if not deleted_row:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to delete bill",
                )

            bill_data = build_bills_post_dict(deleted_row)
            bill = BillsResponse(**bill_data)

            return jsonable_encoder(bill)

        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing bill data",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request",
            ) from e

    def update_bill(self, bill_id: UUID, bills_req: BillsRequest) -> dict:
        try:
            # Check if the bill exists
            if not bills_query.get_bill_by_id(bill_id=bill_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found"
                )

            # Delete the existing bill
            if not bills_query.delete_bill(bill_id):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update bill: deletion error",
                )

            # Insert the updated bill
            updated_row = bills_query.insert_bill(bills_req=bills_req)
            if not updated_row:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update bill: insertion error",
                )

            bill_data = build_bills_post_dict(updated_row)
            bill = BillsResponse(**bill_data)

            return jsonable_encoder(bill)

        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing bill data",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request",
            ) from e

    def update(self, bill_id: UUID, bills_req: BillsRequest) -> dict:
        try:
            # Check if the bill exists
            if not bills_query.get_bill_by_id(bill_id=bill_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found"
                )

            # Update the bill
            updated_row = bills_query.update_bill(bill_id=bill_id, bills_req=bills_req)
            if not updated_row:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update bill",
                )

            bill_data = build_bills_post_dict(updated_row)
            bill = BillsResponse(**bill_data)

            return jsonable_encoder(bill)

        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing bill data",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request",
            ) from e
