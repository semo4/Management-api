from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from src.queries.sections import SectionsQueries
from src.types.sections import SectionsRequest, SectionsResponse
from src.utils.helper import build_section_dict

section_queries = SectionsQueries()


class SectionsServices:
    def get_sections(self) -> jsonable_encoder:
        sections_list = list()
        result = section_queries.get_sections()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No sections Details Found",
            )
        for row in result:
            data = build_section_dict(row)
            sections_list.append(SectionsResponse(**dict(data)))
        content = jsonable_encoder(sections_list)
        return content

    def get_section(self, section_id: UUID) -> jsonable_encoder:
        row = section_queries.get_section(section_id=section_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No section Details Found with this ID: {section_id}",
            )
        data = build_section_dict(row)
        content = jsonable_encoder(SectionsResponse(**dict(data)))
        return content

    def get_section_by_name(self, section_name: str) -> jsonable_encoder:
        row = section_queries.get_section_by_name(section_name=section_name)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No section Details Found with this Name: {section_name}",
            )
        data = build_section_dict(row)
        content = jsonable_encoder(SectionsResponse(**dict(data)))
        return content

    def insert_section(self, section: SectionsRequest) -> jsonable_encoder:
        row = section_queries.insert_section(section=section)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="section Details Inserted failed",
            )
        data = build_section_dict(row)
        content = jsonable_encoder(SectionsResponse(**dict(data)))
        return content

    def delete_section(self, section_id: UUID) -> jsonable_encoder:
        pre_row = section_queries.get_section_by_id(section_id=section_id)
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No section Details Found with this ID: {section_id}",
            )
        else:
            row = section_queries.delete_section(section_id=section_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"section Deleted Failed with this ID: {section_id}",
                )
            data = build_section_dict(row)
            content = jsonable_encoder(SectionsResponse(**dict(data)))
            return content

    def update_section(
        self, section_id: UUID, section: SectionsRequest
    ) -> jsonable_encoder:
        row = section_queries.get_section_by_id(section_id=section_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No section Details Found with this ID: {section_id}",
            )
        else:
            row = section_queries.delete_section(section_id=section_id)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"section Deleted Failed with this ID: {section_id}",
                )
            else:
                row = section_queries.insert_section(section=section)
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="section Details Updated failed",
                    )
                data = build_section_dict(row)
                content = jsonable_encoder(SectionsResponse(**dict(data)))
                return content

    def update(self, section_id: UUID, section: SectionsRequest) -> jsonable_encoder:
        row = section_queries.get_section_by_id(section_id=section_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No section Details Found with this ID: {section_id}",
            )
        else:
            row = section_queries.update_section(section_id=section_id, section=section)
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="section Details Updated failed",
                )
            data = build_section_dict(row)
            content = jsonable_encoder(SectionsResponse(**dict(data)))
            return content
