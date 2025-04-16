from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.queries.covenants import CovenantsCashQueries, CovenantsDevicesQueries
from src.types.covenants import (
    CovenantsCashRequest,
    CovenantsCashResponse,
    CovenantsDevicesRequest,
    CovenantsDevicesResponse,
)
from src.utils.helper import (
    build_covenants_cash_dict,
    build_covenants_cash_post_dict,
    build_covenants_devices_dict,
    build_covenants_devices_post_dict,
)

covenants_cash_queries = CovenantsCashQueries()


class CovenantsCashServices:
    def get_covenants_cash(self) -> List[dict]:
        result = covenants_cash_queries.get_covenants_cash()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No Covenants Cash found"
            )

        try:
            covenants_cash_list = [
                CovenantsCashResponse(**build_covenants_cash_dict(row)).dict()
                for row in result
            ]
            return jsonable_encoder(covenants_cash_list)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing covenants cash data",
            ) from e

    def get_covenant_cash(self, covenant_cash_id: UUID) -> dict:
        row = covenants_cash_queries.get_covenant_cash(
            covenant_cash_id=covenant_cash_id
        )

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Covenant cash not found"
            )

        try:
            covenant_cash_data = build_covenants_cash_dict(row)
            covenant_cash = CovenantsCashResponse(**covenant_cash_data)
            return jsonable_encoder(covenant_cash)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing covenant cash data",
            ) from e

    def get_covenant_cash_by_name(self, covenant_cash_name: str) -> dict:
        row = covenants_cash_queries.get_covenant_cash_by_name(
            covenant_cash_name=covenant_cash_name
        )

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Covenant cash not found"
            )

        try:
            covenant_cash_data = build_covenants_cash_dict(row)
            covenant_cash = CovenantsCashResponse(**covenant_cash_data)
            return jsonable_encoder(covenant_cash)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing covenant cash data",
            ) from e

    def insert_covenant_cash(self, covenants_cash_req: CovenantsCashRequest) -> dict:
        try:
            row = covenants_cash_queries.insert_covenant_cash(
                covenants_cash_req=covenants_cash_req
            )

            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to insert covenant cash details",
                )

            covenant_cash_data = build_covenants_cash_post_dict(row)
            covenant_cash = CovenantsCashResponse(**covenant_cash_data)

            return jsonable_encoder(covenant_cash)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid covenant cash data format",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request",
            ) from e

    def delete_covenant_cash(self, covenant_cash_id: UUID) -> dict:
        try:
            if not covenants_cash_queries.get_covenant_cash_by_id(
                covenant_cash_id=covenant_cash_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Covenant cash not found",
                )

            deleted_row = covenants_cash_queries.delete_covenant_cash(
                covenant_cash_id=covenant_cash_id
            )

            if not deleted_row:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to delete covenant cash",
                )

            covenant_cash_data = build_covenants_cash_post_dict(deleted_row)
            covenant_cash = CovenantsCashResponse(**covenant_cash_data)

            return jsonable_encoder(covenant_cash)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing covenant cash data",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request",
            ) from e

    def update_covenant_cash(
        self, covenant_cash_id: UUID, covenants_cash_req: CovenantsCashRequest
    ) -> dict:
        try:
            if not covenants_cash_queries.get_covenant_cash_by_id(
                covenant_cash_id=covenant_cash_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Covenant cash not found",
                )

            if not covenants_cash_queries.delete_covenant_cash(
                covenant_cash_id=covenant_cash_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update covenant cash: deletion error",
                )

            updated_row = covenants_cash_queries.insert_covenant_cash(
                covenants_cash_req=covenants_cash_req
            )
            if not updated_row:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update covenant cash: insertion error",
                )

            covenant_cash_data = build_covenants_cash_post_dict(updated_row)
            covenant_cash = CovenantsCashResponse(**covenant_cash_data)

            return jsonable_encoder(covenant_cash)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing covenant cash data",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request",
            ) from e

    def update(
        self, covenant_cash_id: UUID, covenants_cash_req: CovenantsCashRequest
    ) -> dict:
        try:
            if not covenants_cash_queries.get_covenant_cash_by_id(
                covenant_cash_id=covenant_cash_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Covenant cash not found",
                )

            updated_row = covenants_cash_queries.update_covenant_cash(
                covenant_cash_id=covenant_cash_id, covenants_cash_req=covenants_cash_req
            )

            if not updated_row:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update covenant cash",
                )

            covenant_cash_data = build_covenants_cash_post_dict(updated_row)
            covenant_cash = CovenantsCashResponse(**covenant_cash_data)

            return jsonable_encoder(covenant_cash)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing covenant cash data",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request",
            ) from e


covenants_devices_queries = CovenantsDevicesQueries()


class CovenantsDevicesServices:
    def get_covenants_devices(self) -> List[dict]:
        result = covenants_devices_queries.get_covenants_devices()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Covenants Devices found",
            )

        try:
            covenants_devices_list = [
                build_covenants_devices_dict(row) for row in result
            ]
            return jsonable_encoder(
                [
                    CovenantsDevicesResponse(**device)
                    for device in covenants_devices_list
                ]
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing covenants devices data",
            ) from e

    def get_covenant_device(self, covenant_device_id: UUID) -> dict:
        row = covenants_devices_queries.get_covenant_device(
            covenant_device_id=covenant_device_id
        )

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Covenant device not found",
            )

        try:
            device_data = build_covenants_devices_dict(row)
            return jsonable_encoder(CovenantsDevicesResponse(**device_data))
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing covenant device data",
            ) from e

    def get_covenant_device_by_name(self, covenant_device_name: str) -> dict:
        row = covenants_devices_queries.get_covenant_device(
            covenant_device_name=covenant_device_name
        )

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Covenant device not found",
            )

        try:
            device_data = build_covenants_devices_dict(row)
            return jsonable_encoder(CovenantsDevicesResponse(**device_data))
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing covenant device data",
            ) from e

    def insert_covenant_device(
        self, covenants_devices_req: CovenantsDevicesRequest
    ) -> dict:
        try:
            row = covenants_devices_queries.insert_covenant_device(
                covenants_devices_req=covenants_devices_req
            )

            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to insert covenant device details",
                )

            device_data = build_covenants_devices_post_dict(row)
            return jsonable_encoder(CovenantsDevicesResponse(**device_data))
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid covenant device data format",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request",
            ) from e

    def delete_covenant_device(self, covenant_device_id: UUID) -> JSONResponse:
        try:
            if not covenants_devices_queries.get_covenant_device_by_id(
                covenant_device_id=covenant_device_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Covenant device not found",
                )

            deleted_row = covenants_devices_queries.delete_covenant_device(
                covenant_device_id=covenant_device_id
            )

            if not deleted_row:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to delete covenant device",
                )

            device_data = build_covenants_devices_post_dict(deleted_row)
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED,
                content=jsonable_encoder(CovenantsDevicesResponse(**device_data)),
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing covenant device data",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request",
            ) from e

    def update_covenant_device(
        self, covenant_device_id: UUID, covenants_devices_req: CovenantsDevicesRequest
    ) -> dict:
        try:
            if not covenants_devices_queries.get_covenant_device_by_id(
                covenant_device_id=covenant_device_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Covenant device not found",
                )

            if not covenants_devices_queries.delete_covenant_device(
                covenant_device_id=covenant_device_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update covenant device: deletion error",
                )

            updated_row = covenants_devices_queries.insert_covenant_device(
                covenants_devices_req=covenants_devices_req
            )
            if not updated_row:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update covenant device: insertion error",
                )

            device_data = build_covenants_devices_post_dict(updated_row)
            return jsonable_encoder(CovenantsDevicesResponse(**device_data))
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing covenant device data",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request",
            ) from e

    def update_device(
        self, covenant_device_id: UUID, covenants_devices_req: CovenantsDevicesRequest
    ) -> dict:
        try:
            if not covenants_devices_queries.get_covenant_device_by_id(
                covenant_device_id=covenant_device_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Covenant device not found",
                )

            updated_row = covenants_devices_queries.update_covenant_device(
                covenant_device_id=covenant_device_id,
                covenants_devices_req=covenants_devices_req,
            )

            if not updated_row:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update covenant device",
                )

            device_data = build_covenants_devices_post_dict(updated_row)
            return jsonable_encoder(CovenantsDevicesResponse(**device_data))
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error processing covenant device data",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request",
            ) from e
