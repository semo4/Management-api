from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder

from src.queries.outcomes_categories import OutcomesCategoriesQueries
from src.types.outcomes_categories import (
    OutcomesCategoriesRequest,
    OutcomesCategoriesResponse,
)
from src.utils.helper import build_response_dict

categories_router = APIRouter(prefix="/categories", tags=["Categories"])

categories_queries = OutcomesCategoriesQueries()


class OutcomesCategoriesServices:
    def get_categories(self) -> jsonable_encoder:
        categories_list = list()
        result = categories_queries.get_categories()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No categories Details Found",
            )
        for row in result:
            data = build_response_dict(row)
            categories_list.append(OutcomesCategoriesResponse(**dict(data)))
        content = jsonable_encoder(categories_list)
        return content

    def get_category(self, categories_id: UUID) -> jsonable_encoder:
        row = categories_queries.get_category(categories_id=categories_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No categories Details Found with this ID: {categories_id}",
            )
        data = build_response_dict(row)
        content = jsonable_encoder(OutcomesCategoriesResponse(**dict(data)))
        return content

    def get_categories_by_title(self, categories_title: str) -> jsonable_encoder:
        row = categories_queries.get_categories_by_title(
            categories_title=categories_title
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No categories Details Found with this Name: {categories_title}",
            )
        data = build_response_dict(row)
        content = jsonable_encoder(OutcomesCategoriesResponse(**dict(data)))
        return content

    def insert_categories(
        self, categories_req: OutcomesCategoriesRequest
    ) -> jsonable_encoder:
        row = categories_queries.insert_categories(categories_req=categories_req)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="categories Details Inserted failed",
            )
        data = build_response_dict(row)
        content = jsonable_encoder(OutcomesCategoriesResponse(**dict(data)))
        return content

    def delete_categories(self, categories_id: UUID) -> jsonable_encoder:
        pre_row = categories_queries.get_category(categories_id=categories_id)
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No categories Details Found with this ID: {categories_id}",
            )
        else:
            row = categories_queries.delete_categories(categories_id=categories_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"categories Deleted Failed with this ID: {categories_id}",
                )
            data = build_response_dict(row)
            content = jsonable_encoder(OutcomesCategoriesResponse(**dict(data)))
            return content

    def update_categories(
        self, categories_id: UUID, categories_req: OutcomesCategoriesRequest
    ) -> jsonable_encoder:
        row = categories_queries.get_category(categories_id=categories_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No categories Details Found with this ID: {categories_id}",
            )
        else:
            row = categories_queries.delete_categories(categories_id=categories_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"categories Deleted Failed with this ID: {categories_id}",
                )
            else:
                row = categories_queries.insert_categories(
                    categories_req=categories_req
                )
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="categories Details Updated failed",
                    )
                data = build_response_dict(row)
                content = jsonable_encoder(OutcomesCategoriesResponse(**dict(data)))
                return content

    def update(self, categories_id: UUID, categories_req: OutcomesCategoriesRequest):
        row = categories_queries.get_category(categories_id=categories_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No categories Details Found with this ID: {categories_id}",
            )
        else:
            row = categories_queries.update_categories(
                categories_id=categories_id, categories_req=categories_req
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="categories Details Updated failed",
                )
            data = build_response_dict(row)
            content = jsonable_encoder(OutcomesCategoriesResponse(**dict(data)))
            return content
