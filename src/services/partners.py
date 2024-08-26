from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from src.queries.partners import PartnersQueries
from src.types.partners import PartnersRequest, PartnersResponse
from src.utils.helper import build_partners_dict, build_partners_post_dict

partners_queries = PartnersQueries()


class PartnersServices:
    def get_partners(self) -> jsonable_encoder:
        partners_list = list()
        result = partners_queries.get_partners()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No partners Details Found",
            )
        for row in result:
            data = build_partners_dict(row)
            partners_list.append(PartnersResponse(**dict(data)))
        content = jsonable_encoder(partners_list)
        return content

    def get_partner(self, partner_id: UUID) -> jsonable_encoder:
        row = partners_queries.get_partner(partner_id=partner_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No partners Details Found with this ID: {partner_id}",
            )
        data = build_partners_dict(row)
        content = jsonable_encoder(PartnersResponse(**dict(data)))
        return content

    def get_partner_by_name(self, partner_name: str) -> jsonable_encoder:
        row = partners_queries.get_partner_by_name(partner_name=partner_name)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No partners Details Found with this Name: {partner_name}",
            )
        data = build_partners_dict(row)
        content = jsonable_encoder(PartnersResponse(**dict(data)))
        return content

    def insert_partner(self, partners_req: PartnersRequest) -> jsonable_encoder:
        row = partners_queries.insert_partner(partners_req=partners_req)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="partners Details Inserted failed",
            )
        data = build_partners_post_dict(row)
        content = jsonable_encoder(PartnersResponse(**dict(data)))
        return content

    def delete_partner(self, partner_id: UUID) -> jsonable_encoder:
        pre_row = partners_queries.get_partner_by_id(partner_id=partner_id)
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No partners Details Found with this ID: {partner_id}",
            )
        else:
            row = partners_queries.delete_partner(partner_id=partner_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"partners Deleted Failed with this ID: {partner_id}",
                )
            data = build_partners_post_dict(row)
            content = jsonable_encoder(PartnersResponse(**dict(data)))
            return content

    def update_partner(
        self, partner_id: UUID, partners_req: PartnersRequest
    ) -> jsonable_encoder:
        row = partners_queries.get_partner_by_id(partner_id=partner_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No partners Details Found with this ID: {partner_id}",
            )
        else:
            row = partners_queries.delete_partner(partner_id=partner_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"partners Deleted Failed with this ID: {partner_id}",
                )
            else:
                row = partners_queries.insert_partner(partners_req=partners_req)
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="partners Details Updated failed",
                    )
                data = build_partners_post_dict(row)
                content = jsonable_encoder(PartnersResponse(**dict(data)))
                return content

    def update(
        self, partner_id: UUID, partners_req: PartnersRequest
    ) -> jsonable_encoder:
        row = partners_queries.get_partner_by_id(partner_id=partner_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No partners Details Found with this ID: {partner_id}",
            )
        else:
            row = partners_queries.update_partner(
                partner_id=partner_id, partners_req=partners_req
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="partners Details Updated failed",
                )
            data = build_partners_post_dict(row)
            content = jsonable_encoder(PartnersResponse(**dict(data)))
            return content
