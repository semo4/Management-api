from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.queries.incomes import IncomesQueries
from src.types.incomes import IncomesRequest, IncomesResponse
from src.utils.helper import build_incomes_dict, build_incomes_dict_post

incomes_queries = IncomesQueries()


class IncomesServices:
    def get_incomes(self) -> jsonable_encoder:
        incomes_list = list()
        result = incomes_queries.get_incomes()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No incomes Details Found"
            )
        for row in result:
            data = build_incomes_dict(row)
            incomes_list.append(IncomesResponse(**dict(data)))
        content = jsonable_encoder(incomes_list)
        return content

    def get_income(self, income_id: UUID) -> jsonable_encoder:
        row = incomes_queries.get_income(income_id=income_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No incomes Details Found with this ID: {income_id}",
            )
        data = build_incomes_dict(row)
        content = jsonable_encoder(IncomesResponse(**dict(data, exclude_none=True)))
        return content

    def get_income_by_receiving_person(
        self, income_receiving_person: str
    ) -> JSONResponse:
        row = incomes_queries.get_income_by_receiving_person(
            income_receiving_person=income_receiving_person
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No incomes Details Found with this Name: {income_receiving_person}",
            )
        data = build_incomes_dict(row)
        content = jsonable_encoder(IncomesResponse(**dict(data)))
        return content

    def get_income_by_gave_person(self, income_gave_person: str) -> jsonable_encoder:
        row = incomes_queries.get_income_by_gave_person(
            income_gave_person=income_gave_person
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No incomes Details Found with this Name: {income_gave_person}",
            )
        data = build_incomes_dict(row)
        content = jsonable_encoder(IncomesResponse(**dict(data)))
        return content

    def get_income_by_check_number(self, income_check_number: int) -> jsonable_encoder:
        row = incomes_queries.get_income_by_check_number(
            income_check_number=income_check_number
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No incomes Details Found with this Name: {income_check_number}",
            )
        data = build_incomes_dict(row)
        content = jsonable_encoder(IncomesResponse(**dict(data)))
        return content

    def get_income_by_way_of_receiving(
        self, income_way_of_receiving: str
    ) -> jsonable_encoder:
        row = incomes_queries.get_income_by_way_of_receiving(
            income_way_of_receiving=income_way_of_receiving
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No incomes Details Found with this Name: {income_way_of_receiving}",
            )
        data = build_incomes_dict(row)
        content = jsonable_encoder(IncomesResponse(**dict(data)))
        return content

    def insert_income(self, incomes_req: IncomesRequest) -> jsonable_encoder:
        row_ = incomes_queries.insert_income(incomes_req=incomes_req)
        if not row_:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="incomes Details Inserted failed",
            )
        row = incomes_queries.get_income(income_id=row_[0])
        data = build_incomes_dict_post(row)
        content = jsonable_encoder(IncomesResponse(**dict(data)))
        return content

    def delete_income(self, income_id: UUID) -> jsonable_encoder:
        pre_row = incomes_queries.get_income_by_id(income_id=income_id)
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No incomes Details Found with this ID: {income_id}",
            )
        else:
            row = incomes_queries.delete_income(income_id=income_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"incomes Deleted Failed with this ID: {income_id}",
                )
            data = build_incomes_dict_post(row)
            content = jsonable_encoder(IncomesResponse(**dict(data)))
            return content

    def update_income(
        self, income_id: UUID, incomes_req: IncomesRequest
    ) -> jsonable_encoder:
        row = incomes_queries.get_income_by_id(income_id=income_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No incomes Details Found with this ID: {income_id}",
            )
        else:
            row = incomes_queries.delete_income(income_id=income_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"incomes Deleted Failed with this ID: {income_id}",
                )
            else:
                row = incomes_queries.insert_income(incomes_req=incomes_req)
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="incomes Details Updated failed",
                    )
                data = build_incomes_dict_post(row)
                content = jsonable_encoder(IncomesResponse(**dict(data)))
                return content

    def update(self, income_id: UUID, incomes_req: IncomesRequest):
        row = incomes_queries.get_income_by_id(income_id=income_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No incomes Details Found with this ID: {income_id}",
            )
        else:
            row = incomes_queries.update_income(
                income_id=income_id, incomes_req=incomes_req
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="incomes Details Updated failed",
                )
            data = build_incomes_dict_post(row)
            content = jsonable_encoder(IncomesResponse(**dict(data)))
            return content
