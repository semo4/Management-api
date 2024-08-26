from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from src.queries.contractors import ContractorsQueries
from src.types.contractors import ContractorsRequest, ContractorsResponse
from src.utils.helper import build_contractors_dict, build_contractors_dict_post

contractors_queries = ContractorsQueries()


class ContractorsServices:
    def get_contractors(self) -> List[dict]:
        result = contractors_queries.get_contractors()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No contractors found"
            )

        try:
            contractors_list = [
                ContractorsResponse(**build_contractors_dict(row)) for row in result
            ]
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing contractor data",
            ) from e

        return jsonable_encoder(contractors_list)

    def get_contractor(self, contractor_id: UUID) -> dict:
        row = contractors_queries.get_contractor(contractor_id=contractor_id)

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Contractor not found"
            )

        try:
            contractor_data = build_contractors_dict(row)
            contractor = ContractorsResponse(**contractor_data)
            return jsonable_encoder(contractor.dict(exclude_none=True))
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing contractor data",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred",
            ) from e

    def get_contractor_by_name(self, contractor_name: str) -> dict:
        row = contractors_queries.get_contractor_by_name(
            contractor_name=contractor_name
        )

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Contractor not found"
            )

        try:
            contractor_data = build_contractors_dict(row)
            contractor = ContractorsResponse(**contractor_data)
            return jsonable_encoder(contractor)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing contractor data",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred",
            ) from e

    def insert_contractor(self, contractors_req: ContractorsRequest) -> dict:
        try:
            row = contractors_queries.insert_contractor(contractors_req=contractors_req)

            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to insert contractor details",
                )

            contractor_data = build_contractors_dict_post(row)
            contractor = ContractorsResponse(**contractor_data)

            return jsonable_encoder(contractor)

        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid contractor data format",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request",
            ) from e

    def delete_contractor(self, contractor_id: UUID) -> dict:
        try:
            # Check if the contractor exists
            if not contractors_queries.get_contractor_by_id(
                contractor_id=contractor_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Contractor not found"
                )

            # Attempt to delete the contractor
            deleted_row = contractors_queries.delete_contractor(
                contractor_id=contractor_id
            )

            if not deleted_row:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to delete contractor",
                )

            contractor_data = build_contractors_dict_post(deleted_row)
            contractor = ContractorsResponse(**contractor_data)

            return jsonable_encoder(contractor)

        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing contractor data",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request",
            ) from e

    def update_contractor(
        self, contractor_id: UUID, contractors_req: ContractorsRequest
    ) -> dict:
        try:
            # Check if the contractor exists
            if not contractors_queries.get_contractor_by_id(
                contractor_id=contractor_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Contractor not found"
                )

            # Delete the existing contractor
            if not contractors_queries.delete_contractor(contractor_id=contractor_id):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update contractor: deletion error",
                )

            # Insert the updated contractor
            updated_row = contractors_queries.insert_contractor(
                contractors_req=contractors_req
            )
            if not updated_row:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update contractor: insertion error",
                )

            contractor_data = build_contractors_dict_post(updated_row)
            contractor = ContractorsResponse(**contractor_data)

            return jsonable_encoder(contractor)

        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing contractor data",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request",
            ) from e

    def update(self, contractor_id: UUID, contractors_req: ContractorsRequest) -> dict:
        try:
            # Check if the contractor exists
            if not contractors_queries.get_contractor_by_id(
                contractor_id=contractor_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Contractor not found"
                )

            # Update the contractor
            updated_row = contractors_queries.update_contractor(
                contractor_id=contractor_id, contractors_req=contractors_req
            )

            if not updated_row:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update contractor",
                )

            contractor_data = build_contractors_dict_post(updated_row)
            contractor = ContractorsResponse(**contractor_data)

            return jsonable_encoder(contractor)

        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing contractor data",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request",
            ) from e
