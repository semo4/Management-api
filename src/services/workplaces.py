from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from src.queries.workplaces import WorkPlaceQueries
from src.types.workplaces import WorkPlacesRequest, WorkPlacesResponse
from src.utils.helper import build_response_dict

workplace_queries = WorkPlaceQueries()


class WorkPlaceServices:
    def get_workplaces(self) -> jsonable_encoder:
        workplace_list = list()
        result = workplace_queries.get_workplaces()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No workplace Details Found",
            )
        for row in result:
            data = build_response_dict(row)
            workplace_list.append(WorkPlacesResponse(**dict(data)))
        content = jsonable_encoder(workplace_list)
        return content

    def get_workplace(self, workplace_id: UUID) -> jsonable_encoder:
        row = workplace_queries.get_workplace(workplace_id=workplace_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No workplace Details Found with this ID: {workplace_id}",
            )
        data = build_response_dict(row)
        content = jsonable_encoder(WorkPlacesResponse(**dict(data)))
        return content

    def get_workplace_by_title(self, workplace_title: str) -> jsonable_encoder:
        row = workplace_queries.get_workplace_by_title(workplace_title=workplace_title)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No workplace Details Found with this Name: {workplace_title}",
            )
        data = build_response_dict(row)
        content = jsonable_encoder(WorkPlacesResponse(**dict(data)))
        return content

    def insert_workplace(self, workplace_req: WorkPlacesRequest) -> jsonable_encoder:
        row = workplace_queries.insert_workplace(workplace_req=workplace_req)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="workplace Details Inserted failed",
            )
        data = build_response_dict(row)
        content = jsonable_encoder(WorkPlacesResponse(**dict(data)))
        return content

    def delete_workplace(self, workplace_id: UUID) -> jsonable_encoder:
        pre_row = workplace_queries.get_workplace_by_id(workplace_id=workplace_id)
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No workplace Details Found with this ID: {workplace_id}",
            )
        else:
            row = workplace_queries.delete_workplace(workplace_id=workplace_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"workplace Deleted Failed with this ID: {workplace_id}",
                )
            data = build_response_dict(row)
            content = jsonable_encoder(WorkPlacesResponse(**dict(data)))
            return content

    def update_workplace(
        self, workplace_id: UUID, workplace_req: WorkPlacesRequest
    ) -> jsonable_encoder:
        row = workplace_queries.get_workplace_by_id(workplace_id=workplace_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No workplace Details Found with this ID: {workplace_id}",
            )
        else:
            row = workplace_queries.delete_workplace(workplace_id=workplace_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"workplace Deleted Failed with this ID: {workplace_id}",
                )
            else:
                row = workplace_queries.insert_workplace(workplace_req=workplace_req)
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="workplace Details Updated failed",
                    )
                data = build_response_dict(row)
                content = jsonable_encoder(WorkPlacesResponse(**dict(data)))
                return content

    def update(
        self, workplace_id: UUID, workplace_req: WorkPlacesRequest
    ) -> jsonable_encoder:
        row = workplace_queries.get_workplace_by_id(workplace_id=workplace_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No workplace Details Found with this ID: {workplace_id}",
            )
        else:
            row = workplace_queries.update_workplace(
                workplace_id=workplace_id, workplace_req=workplace_req
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="workplace Details Updated failed",
                )
            data = build_response_dict(row)
            content = jsonable_encoder(WorkPlacesResponse(**dict(data)))
            return content
