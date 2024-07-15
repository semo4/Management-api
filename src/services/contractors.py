from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from src.queries.contractors import ContractorsQueries
from src.types.contractors import ContractorsRequest, ContractorsResponse
from src.utils.helper import build_contractors_dict, build_contractors_dict_post

contractors_queries = ContractorsQueries()


class ContractorsServices:
    def get_contractors(self) -> jsonable_encoder:
        contractors_list = list()
        result = contractors_queries.get_contractors()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No contractors Details Found",
            )
        for row in result:
            data = build_contractors_dict(row)
            contractors_list.append(data)
        content = jsonable_encoder(
            ContractorsResponse(**dict(i)) for i in contractors_list
        )
        return content

    def get_contractor(self, contractor_id: UUID) -> jsonable_encoder:
        row = contractors_queries.get_contractor(contractor_id=contractor_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No contractors Details Found with this ID: {contractor_id}",
            )
        data = build_contractors_dict(row)
        content = jsonable_encoder(ContractorsResponse(**dict(data, exclude_none=True)))
        return content

    def get_contractor_by_name(self, contractor_name: str) -> jsonable_encoder:
        row = contractors_queries.get_contractor_by_name(
            contractor_name=contractor_name
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No contractors Details Found with this Name: {contractor_name}",
            )
        data = build_contractors_dict(row)
        content = jsonable_encoder(ContractorsResponse(**dict(data)))
        return content

    def insert_contractor(
        self, contractors_req: ContractorsRequest
    ) -> jsonable_encoder:
        row = contractors_queries.insert_contractor(contractors_req=contractors_req)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="contractors Details Inserted failed",
            )
        data = build_contractors_dict_post(row)
        content = jsonable_encoder(ContractorsResponse(**dict(data)))
        return content

    def delete_contractor(self, contractor_id: UUID) -> jsonable_encoder:
        pre_row = contractors_queries.get_contractor_by_id(contractor_id=contractor_id)
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No contractors Details Found with this ID: {contractor_id}",
            )
        else:
            row = contractors_queries.delete_contractor(contractor_id=contractor_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"contractors Deleted Failed with this ID: {contractor_id}",
                )
            data = build_contractors_dict_post(row)
            content = jsonable_encoder(ContractorsResponse(**dict(data)))
            return content

    def update_contractor(
        self, contractor_id: UUID, contractors_req: ContractorsRequest
    ) -> jsonable_encoder:
        row = contractors_queries.get_contractor_by_id(contractor_id=contractor_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No contractors Details Found with this ID: {contractor_id}",
            )
        else:
            row = contractors_queries.delete_contractor(contractor_id=contractor_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"contractors Deleted Failed with this ID: {contractor_id}",
                )
            else:
                row = contractors_queries.insert_contractor(
                    contractors_req=contractors_req
                )
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="contractors Details Updated failed",
                    )
                data = build_contractors_dict_post(row)
                content = jsonable_encoder(ContractorsResponse(**dict(data)))
                return content

    def update(
        self,
        contractor_id: UUID,
        contractors_req: ContractorsRequest,
    ) -> jsonable_encoder:
        row = contractors_queries.get_contractor_by_id(contractor_id=contractor_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No contractors Details Found with this ID: {contractor_id}",
            )
        else:
            row = contractors_queries.update_contractor(
                contractor_id=contractor_id, contractors_req=contractors_req
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="contractors Details Updated failed",
                )
            data = build_contractors_dict_post(row)
            content = jsonable_encoder(ContractorsResponse(**dict(data)))
            return content
