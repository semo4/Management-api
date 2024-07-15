from uuid import UUID

from sqlalchemy.sql import select

from src.database.connection import execute_all, execute_one
from src.database.database import ALL_COLUMNS
from src.models.covenants import covenants_cash, covenants_devices
from src.models.partners import partners
from src.models.workers import workers
from src.types.covenants import CovenantsCashRequest, CovenantsDevicesRequest


class CovenantsCashQueries:
    def get_covenants_cash(self):
        join_table = covenants_cash.join(
            partners, covenants_cash.c.partner_id == partners.c.id
        )
        res = (
            select(covenants_cash, partners.c.name)
            .select_from(join_table)
            .where(covenants_cash.c.partner_id == partners.c.id)
        )
        result = execute_all(res)
        return result

    def get_covenant_cash(self, covenant_cash_id: UUID):
        join_table = covenants_cash.join(
            partners, covenants_cash.c.partner_id == partners.c.id
        )
        result = (
            select(covenants_cash, partners.c.name)
            .select_from(join_table)
            .where(covenants_cash.c.partner_id == partners.c.id)
            .where(covenants_cash.c.id == covenant_cash_id)
        )
        row = execute_one(result)
        return row

    def get_covenant_cash_by_id(self, covenant_cash_id: UUID):
        result = covenants_cash.select().where(covenants_cash.c.id == covenant_cash_id)
        row = execute_one(result)
        return row

    def get_covenant_cash_by_name(self, covenant_cash_name: str):
        result = (
            select(covenants_cash, partners.c.name)
            .select_from(
                covenants_cash.join(
                    partners, covenants_cash.c.partner_id == partners.c.id
                )
            )
            .where(covenants_cash.c.partner_id == partners.c.id)
            .where(covenants_cash.c.name == covenant_cash_name)
        )
        row = execute_one(result)
        return row

    def insert_covenant_cash(self, covenants_cash_req: CovenantsCashRequest):
        result = (
            covenants_cash.insert()
            .values(dict(covenants_cash_req))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def delete_covenant_cash(self, covenant_cash_id: UUID):
        result = (
            covenants_cash.delete()
            .where(covenants_cash.c.id == covenant_cash_id)
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_covenant_cash(
        self, covenant_cash_id: UUID, covenants_cash_req: CovenantsCashRequest
    ):
        result = (
            covenants_cash.update()
            .where(covenants_cash.c.id == covenant_cash_id)
            .values(dict(covenants_cash_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row


class CovenantsDevicesQueries:
    def get_covenants_devices(self):
        join_table = covenants_devices.join(
            workers, covenants_devices.c.worker_id == workers.c.id
        )
        res = (
            select(covenants_devices, workers.c.name)
            .select_from(join_table)
            .where(covenants_devices.c.worker_id == workers.c.id)
        )
        result = execute_all(res)
        return result

    def get_covenant_device(self, covenant_device_id: UUID):
        join_table = covenants_devices.join(
            workers, covenants_devices.c.worker_id == workers.c.id
        )
        result = (
            select(covenants_devices, workers.c.name)
            .select_from(join_table)
            .where(covenants_devices.c.worker_id == workers.c.id)
            .where(covenants_devices.c.id == covenant_device_id)
        )
        row = execute_one(result)
        return row

    def get_covenant_device_by_name(self, covenant_device_name: str):
        result = (
            select(covenants_devices, workers.c.name)
            .select_from(
                covenants_devices.join(
                    workers, covenants_devices.c.worker_id == workers.c.id
                )
            )
            .where(covenants_devices.c.worker_id == workers.c.id)
            .where(covenants_devices.c.title == covenant_device_name)
        )
        row = execute_one(result)
        return row

    def get_covenant_device_by_id(self, covenant_device_id: UUID):
        result = covenants_devices.select().where(
            covenants_devices.c.id == covenant_device_id
        )
        row = execute_one(result)
        return row

    def insert_covenant_device(self, covenants_devices_req: CovenantsDevicesRequest):
        result = (
            covenants_devices.insert()
            .values(dict(covenants_devices_req))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def delete_covenant_device(self, covenant_device_id: UUID):
        result = (
            covenants_devices.delete()
            .where(covenants_devices.c.id == covenant_device_id)
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row

    def update_covenant_device(
        self, covenant_device_id: UUID, covenants_devices_req: CovenantsDevicesRequest
    ):
        result = (
            covenants_devices.update()
            .where(covenants_devices.c.id == covenant_device_id)
            .values(dict(covenants_devices_req.dict(exclude_unset=True)))
            .returning(ALL_COLUMNS)
        )
        row = execute_one(result)
        return row
