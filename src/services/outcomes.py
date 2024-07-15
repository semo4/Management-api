from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from src.queries.outcomes import OutcomesQueries
from src.types.outcomes import OutcomesRequest, OutcomesResponse
from src.utils.helper import build_outcomes_dict, build_outcomes_dict_post

outcomes_queries = OutcomesQueries()


class OutcomesServices:
    def get_outcomes(self) -> jsonable_encoder:
        outcomes_list = list()
        result = outcomes_queries.get_outcomes()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No outcomes Details Found",
            )
        for row in result:
            data = build_outcomes_dict(row)
            outcomes_list.append(data)
        content = jsonable_encoder(OutcomesResponse(**dict(i)) for i in outcomes_list)
        return content

    def get_outcome(self, outcome_id: UUID) -> jsonable_encoder:
        row = outcomes_queries.get_outcome(outcome_id=outcome_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No outcomes Details Found with this ID: {outcome_id}",
            )
        data = build_outcomes_dict(row)
        content = jsonable_encoder(OutcomesResponse(**dict(data, exclude_none=True)))
        return content

    def get_outcome_by_buyer_name(self, outcome_buyer_name: str) -> jsonable_encoder:
        row = outcomes_queries.get_outcome_by_buyer_name(
            outcome_buyer_name=outcome_buyer_name
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No outcomes Details Found with this Name: {outcome_buyer_name}",
            )
        data = build_outcomes_dict(row)
        content = jsonable_encoder(OutcomesResponse(**dict(data)))
        return content

    def get_outcome_by_amount_payed(outcome_amount_payed: float) -> jsonable_encoder:
        row = outcomes_queries.get_outcome_by_amount_payed(
            outcome_amount_payed=outcome_amount_payed
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No outcomes Details Found with this Name: {outcome_amount_payed}",
            )
        data = build_outcomes_dict(row)
        content = jsonable_encoder(OutcomesResponse(**dict(data)))
        return content

    def get_outcome_by_date(self, outcome_date: datetime) -> jsonable_encoder:
        row = outcomes_queries.get_outcome_by_date(outcome_date=outcome_date)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No outcomes Details Found with this Name: {outcome_date}",
            )
        data = build_outcomes_dict(row)
        content = jsonable_encoder(OutcomesResponse(**dict(data)))
        return content

    def insert_outcome(self, outcomes_req: OutcomesRequest) -> jsonable_encoder:
        row_ = outcomes_queries.insert_outcome(outcomes_req=outcomes_req)
        if not row_:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="outcomes Details Inserted failed",
            )
        row = outcomes_queries.get_outcome(outcome_id=row_[0])
        data = build_outcomes_dict_post(row)
        content = jsonable_encoder(OutcomesResponse(**dict(data)))
        return content

    def delete_outcome(self, outcome_id: UUID) -> jsonable_encoder:
        pre_row = outcomes_queries.get_outcome_by_id(outcome_id=outcome_id)
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No outcomes Details Found with this ID: {outcome_id}",
            )
        else:
            row = outcomes_queries.delete_outcome(outcome_id=outcome_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"outcomes Deleted Failed with this ID: {outcome_id}",
                )
            data = build_outcomes_dict_post(row)
            content = jsonable_encoder(OutcomesResponse(**dict(data)))
            return content

    def update_outcome(
        self, outcome_id: UUID, outcomes_req: OutcomesRequest
    ) -> jsonable_encoder:
        row = outcomes_queries.get_outcome_by_id(outcome_id=outcome_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No outcomes Details Found with this ID: {outcome_id}",
            )
        else:
            row = outcomes_queries.delete_outcome(outcome_id=outcome_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"outcomes Deleted Failed with this ID: {outcome_id}",
                )
            else:
                row = outcomes_queries.insert_outcome(outcomes_req=outcomes_req)
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="outcomes Details Updated failed",
                    )
                data = build_outcomes_dict_post(row)
                content = jsonable_encoder(OutcomesResponse(**dict(data)))
                return content

    def update(self, outcome_id: UUID, outcomes_req: OutcomesRequest):
        row = outcomes_queries.get_outcome_by_id(outcome_id=outcome_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No outcomes Details Found with this ID: {outcome_id}",
            )
        else:
            row = outcomes_queries.update_outcome(
                outcome_id=outcome_id, outcomes_req=outcomes_req
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="outcomes Details Updated failed",
                )
            data = build_outcomes_dict_post(row)
            content = jsonable_encoder(OutcomesResponse(**dict(data)))
            return content
