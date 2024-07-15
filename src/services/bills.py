from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from src.queries.bills import BillsQueries
from src.types.bills import BillsRequest, BillsResponse
from src.utils.helper import build_bills_dict, build_bills_post_dict

bills_query = BillsQueries()


class BillsServices:
    def get_bills(self) -> jsonable_encoder:
        bills_list = list()
        result = bills_query.get_bills()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No bills Details Found"
            )
        for row in result:
            data = build_bills_dict(row)
            bills_list.append(data)
            # bills_list.append(BillsResponse(**dict(data)))
        content = jsonable_encoder(BillsResponse(**dict(i)) for i in bills_list)
        # content = jsonable_encoder(bills_list)
        return content

    def get_bill(self, bill_id: UUID) -> jsonable_encoder:
        row = bills_query.get_bill(bill_id=bill_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No bills Details Found with this ID: {bill_id}",
            )
        data = build_bills_dict(row)
        content = jsonable_encoder(BillsResponse(**dict(data)))
        return content

    def get_bill_by_name(self, bill_store_name: str) -> jsonable_encoder:
        row = bills_query.get_bill_by_name(bill_store_name=bill_store_name)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No bills Details Found with this Name: {bill_store_name}",
            )
        data = build_bills_dict(row)
        content = jsonable_encoder(BillsResponse(**dict(data)))
        return content

    def get_bill_by_buyer_name(self, bill_buyer_name: str) -> jsonable_encoder:
        row = bills_query.get_bill_by_buyer_name(bill_buyer_name=bill_buyer_name)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No bills Details Found with this Name: {bill_buyer_name}",
            )
        data = build_bills_dict(row)
        content = jsonable_encoder(BillsResponse(**dict(data)))
        return content

    def get_bill_by_bill_number(self, bill_number: int) -> jsonable_encoder:
        row = bills_query.get_bill_by_bill_number(bill_number=bill_number)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No bills Details Found with this Name: {bill_number}",
            )
        data = build_bills_dict(row)
        content = jsonable_encoder(BillsResponse(**dict(data)))
        return content

    def insert_bill(self, bills_req: BillsRequest) -> jsonable_encoder:
        row = bills_query.insert_bill(bills_req=bills_req)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="bills Details Inserted failed",
            )
        data = build_bills_post_dict(row)
        content = jsonable_encoder(BillsResponse(**dict(data)))
        return content

    def delete_bill(self, bill_id: UUID) -> jsonable_encoder:
        pre_row = bills_query.get_bill_by_id(bill_id=bill_id)
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No bills Details Found with this ID: {bill_id}",
            )
        else:
            row = bills_query.delete_bill(bill_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"bills Deleted Failed with this ID: {bill_id}",
                )
            data = build_bills_post_dict(row)
            content = jsonable_encoder(BillsResponse(**dict(data)))
            return content

    def update_bill(self, bill_id: UUID, bills_req: BillsRequest) -> jsonable_encoder:
        row = bills_query.get_bill_by_id(bill_id=bill_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No bills Details Found with this ID: {bill_id}",
            )
        else:
            row = bills_query.delete_bill(bill_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"bills Deleted Failed with this ID: {bill_id}",
                )
            else:
                row = bills_query.insert_bill(bills_req=bills_req)
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="bills Details Updated failed",
                    )
                data = build_bills_post_dict(row)
                content = jsonable_encoder(BillsResponse(**dict(data)))
                return content

    def update(self, bill_id: UUID, bills_req: BillsRequest) -> jsonable_encoder:
        row = bills_query.get_bill_by_id(bill_id=bill_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No bills Details Found with this ID: {bill_id}",
            )
        else:
            row = bills_query.update_bill(bill_id=bill_id, bills_req=bills_req)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="bills Details Updated failed",
                )
            data = build_bills_post_dict(row)
            content = jsonable_encoder(BillsResponse(**dict(data)))
            return content
