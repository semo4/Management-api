from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from src.queries.salaries import SalariesQueries
from src.types.salaries import SalariesRequest, SalariesResponse
from src.utils.helper import build_salaries_dict, build_salaries_dict_post

salaries_queries = SalariesQueries()


class SalariesServices:
    def get_salaries(self) -> jsonable_encoder:
        salaries_list = list()
        result = salaries_queries.get_salaries()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No salaries Details Found",
            )
        for row in result:
            data = build_salaries_dict(row)
            salaries_list.append(SalariesResponse(**dict(data)))
        content = jsonable_encoder(salaries_list)
        return content

    def get_salary(self, salaries_id: UUID) -> jsonable_encoder:
        row = salaries_queries.get_salary(salaries_id=salaries_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No salaries Details Found with this ID: {salaries_id}",
            )
        data = build_salaries_dict(row)
        content = jsonable_encoder(SalariesResponse(**dict(data)))
        return content

    def get_salary_by_salary_type(self, salary_type: str) -> jsonable_encoder:
        row = salaries_queries.get_salary_by_salary_type(salary_type=salary_type)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No salaries Details Found with this ID: {salary_type}",
            )
        data = build_salaries_dict(row)
        content = jsonable_encoder(SalariesResponse(**dict(data)))
        return content

    def insert_salary(self, salaries_req: SalariesRequest) -> jsonable_encoder:
        row = salaries_queries.insert_salary(salaries_req=salaries_req)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="salaries Details Inserted failed",
            )
        data = build_salaries_dict_post(row)
        content = jsonable_encoder(SalariesResponse(**dict(data)))
        return content

    def delete_salary(self, salaries_id: UUID) -> jsonable_encoder:
        pre_row = salaries_queries.get_salary_by_id(salaries_id=salaries_id)
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No salaries Details Found with this ID: {salaries_id}",
            )
        else:
            row = salaries_queries.delete_salary(salaries_id=salaries_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"salaries Deleted Failed with this ID: {salaries_id}",
                )
            data = build_salaries_dict_post(row)
            content = jsonable_encoder(SalariesResponse(**dict(data)))
            return content

    def update_salary(
        self, salaries_id: UUID, salaries_req: SalariesRequest
    ) -> jsonable_encoder:
        row = salaries_queries.get_salary_by_id(salaries_id=salaries_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No salaries Details Found with this ID: {salaries_id}",
            )
        else:
            row = salaries_queries.delete_salary(salaries_id=salaries_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"salaries Deleted Failed with this ID: {salaries_id}",
                )
            else:
                row = salaries_queries.insert_salary(salaries_req=salaries_req)
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="salaries Details Updated failed",
                    )
                data = build_salaries_dict_post(row)
                content = jsonable_encoder(SalariesResponse(**dict(data)))
                return content

    def update(
        self, salaries_id: UUID, salaries_req: SalariesRequest
    ) -> jsonable_encoder:
        row = salaries_queries.get_salary_by_id(salaries_id=salaries_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No salaries Details Found with this ID: {salaries_id}",
            )
        else:
            row = salaries_queries.update_salary(
                salaries_id=salaries_id, salaries_req=salaries_req
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="salaries Details Updated failed",
                )
            data = build_salaries_dict_post(row)
            content = jsonable_encoder(SalariesResponse(**dict(data)))
            return content
