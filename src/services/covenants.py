from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

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
    def get_covenants_cash(self) -> jsonable_encoder:
        covenants_cash_list = list()
        result = covenants_cash_queries.get_covenants_cash()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Covenants Cash Details Found",
            )
        for row in result:
            data = build_covenants_cash_dict(row)
            covenants_cash_list.append(CovenantsCashResponse(**dict(data)))
        content = jsonable_encoder(covenants_cash_list)
        return content

    def get_covenant_cash(self, covenant_cash_id: UUID) -> jsonable_encoder:
        row = covenants_cash_queries.get_covenant_cash(
            covenant_cash_id=covenant_cash_id
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Covenants Cash Details Found with this ID: {covenant_cash_id}",
            )
        data = build_covenants_cash_dict(row)
        content = jsonable_encoder(CovenantsCashResponse(**dict(data)))
        return content

    def get_covenant_cash_by_name(self, covenant_cash_name: str) -> jsonable_encoder:
        row = covenants_cash_queries.get_covenant_cash_by_name(
            covenant_cash_name=covenant_cash_name
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Covenants Cash Details Found with this Name: {covenant_cash_name}",
            )
        data = build_covenants_cash_dict(row)
        content = jsonable_encoder(CovenantsCashResponse(**dict(data)))
        return content

    def insert_covenant_cash(
        self, covenants_cash_req: CovenantsCashRequest
    ) -> jsonable_encoder:
        row = covenants_cash_queries.insert_covenant_cash(
            covenants_cash_req=covenants_cash_req
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Covenants Cash Details Inserted failed",
            )
        data = build_covenants_cash_post_dict(row)
        content = jsonable_encoder(CovenantsCashResponse(**dict(data)))
        return content

    def delete_covenant_cash(self, covenant_cash_id: UUID) -> jsonable_encoder:
        pre_row = covenants_cash_queries.get_covenant_cash_by_id(
            covenant_cash_id=covenant_cash_id
        )
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Covenants Cash Details Found with this ID: {covenant_cash_id}",
            )
        else:
            row = covenants_cash_queries.delete_covenant_cash(
                covenant_cash_id=covenant_cash_id
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"covenants_cash Deleted Failed with this ID: {covenant_cash_id}",
                )
            data = build_covenants_cash_post_dict(row)
            content = jsonable_encoder(CovenantsCashResponse(**dict(data)))
            return content

    def update_covenant_cash(
        self, covenant_cash_id: UUID, covenants_cash_req: CovenantsCashRequest
    ) -> jsonable_encoder:
        row = covenants_cash_queries.get_covenant_cash_by_id(
            covenant_cash_id=covenant_cash_id
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Covenants Cash Details Found with this ID: {covenant_cash_id}",
            )
        else:
            row = covenants_cash_queries.delete_covenant_cash(
                covenant_cash_id=covenant_cash_id
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"covenants_cash Deleted Failed with this ID: {covenant_cash_id}",
                )
            else:
                row = covenants_cash_queries.insert_covenant_cash(
                    covenants_cash_req=covenants_cash_req
                )
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Covenants Cash Details Updated failed",
                    )
                data = build_covenants_cash_post_dict(row)
                content = jsonable_encoder(CovenantsCashResponse(**dict(data)))
                return content

    def update(
        self, covenant_cash_id: UUID, covenants_cash_req: CovenantsCashRequest
    ) -> jsonable_encoder:
        row = covenants_cash_queries.get_covenant_cash_by_id(
            covenant_cash_id=covenant_cash_id
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Covenants Cash Details Found with this ID: {covenant_cash_id}",
            )
        else:
            row = covenants_cash_queries.update_covenant_cash(
                covenant_cash_id=covenant_cash_id, covenants_cash_req=covenants_cash_req
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Covenants Cash Details Updated failed",
                )
            data = build_covenants_cash_post_dict(row)
            content = jsonable_encoder(CovenantsCashResponse(**dict(data)))
            return content


covenants_devices_queries = CovenantsDevicesQueries()


class CovenantsDevicesServices:
    def get_covenants_devices(self) -> jsonable_encoder:
        covenants_devices_list = list()
        result = covenants_devices_queries.get_covenants_devices()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Covenants Devices Details Found",
            )
        for row in result:
            data = build_covenants_devices_dict(row)
            covenants_devices_list.append(data)
        content = jsonable_encoder(
            CovenantsDevicesResponse(**dict(i)) for i in covenants_devices_list
        )
        return content

    def get_covenant_device(self, covenant_device_id: UUID) -> jsonable_encoder:
        row = covenants_devices_queries.get_covenant_device(
            covenant_device_id=covenant_device_id
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Covenants Devices Details Found with this ID: {covenant_device_id}",
            )
        data = build_covenants_devices_dict(row)
        content = jsonable_encoder(CovenantsDevicesResponse(**dict(data)))
        return content

    def get_covenant_device_by_name(
        self, covenant_device_name: str
    ) -> jsonable_encoder:
        row = covenants_devices_queries.get_covenant_device(
            covenant_device_name=covenant_device_name
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Covenants Devices Details Found with this Name: {covenant_device_name}",
            )
        data = build_covenants_devices_dict(row)
        content = jsonable_encoder(CovenantsDevicesResponse(**dict(data)))
        return content

    def insert_covenant_device(
        self, covenants_devices_req: CovenantsDevicesRequest
    ) -> jsonable_encoder:
        row = covenants_devices_queries.insert_covenant_device(
            covenants_devices_req=covenants_devices_req
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Covenants Devices Details Inserted failed",
            )
        data = build_covenants_devices_post_dict(row)
        content = jsonable_encoder(CovenantsDevicesResponse(**dict(data)))
        return content

    def delete_covenant_device(self, covenant_device_id: UUID) -> JSONResponse:
        pre_row = covenants_devices_queries.get_covenant_device_by_id(
            covenant_device_id=covenant_device_id
        )
        if not pre_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Covenants Devices Details Found with this ID: {covenant_device_id}",
            )
        else:
            row = covenants_devices_queries.delete_covenant_device(
                covenant_device_id=covenant_device_id
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"covenants_devices Deleted Failed with this ID: {covenant_device_id}",
                )
            data = build_covenants_devices_post_dict(row)
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED,
                content=jsonable_encoder(CovenantsDevicesResponse(**dict(data))),
            )

    def update_covenant_device(
        self, covenant_device_id: UUID, covenants_devices_req: CovenantsDevicesRequest
    ) -> jsonable_encoder:
        row = covenants_devices_queries.get_covenant_device_by_id(
            covenant_device_id=covenant_device_id
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Covenants Devices Details Found with this ID: {covenant_device_id}",
            )
        else:
            row = covenants_devices_queries.delete_covenant_device(
                covenant_device_id=covenant_device_id
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"covenants_devices Deleted Failed with this ID: {covenant_device_id}",
                )
            else:
                row = covenants_devices_queries.insert_covenant_device(
                    covenants_devices_req=covenants_devices_req
                )
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Covenants Devices Details Updated failed",
                    )
                data = build_covenants_devices_post_dict(row)
                content = jsonable_encoder(CovenantsDevicesResponse(**dict(data)))
                return content

    def update_device(
        self, covenant_device_id: UUID, covenants_devices_req: CovenantsDevicesRequest
    ) -> jsonable_encoder:
        row = covenants_devices_queries.get_covenant_device_by_id(
            covenant_device_id=covenant_device_id
        )
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Covenants Devices Details Found with this ID: {covenant_device_id}",
            )
        else:
            row = covenants_devices_queries.update_covenant_device(
                covenant_device_id=covenant_device_id,
                covenants_devices_req=covenants_devices_req,
            )
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Covenants Devices Details Updated failed",
                )
            data = build_covenants_devices_post_dict(row)
            content = jsonable_encoder(CovenantsDevicesResponse(**dict(data)))
            return content
