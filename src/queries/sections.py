from uuid import UUID

from src.database.connection import execute_all, execute_one
from src.database.database import ALL_COLUMNS
from src.models.sections import sections
from src.types.sections import SectionsRequest


class SectionsQueries:
    def get_sections(self):
        result = execute_all(sections.select())
        return result

    def get_section(self, section_id: UUID):
        result = sections.select().where(sections.c.id == section_id)
        row = execute_one(result)
        return row

    def get_section_by_name(self, section_name: str):
        result = sections.select().where(sections.c.name == section_name)
        row = execute_one(result)
        return row

    def insert_section(self, section: SectionsRequest):
        result = sections.insert().values(dict(section)).returning(ALL_COLUMNS)
        row = execute_one(result)
        return row

    def get_section_by_id(self, section_id: UUID):
        result = sections.select().where(sections.c.id == section_id)
        row = execute_one(result)
        return row

    def delete_section(self, section_id: UUID):
        result = (
            sections.delete().where(sections.c.id == section_id).returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_section(self, section_id: UUID, section: SectionsRequest):
        result = (
            sections.update()
            .where(sections.c.id == section_id)
            .values(dict(section.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row
