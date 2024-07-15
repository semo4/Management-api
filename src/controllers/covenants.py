from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.oauth2 import get_current_user
from src.services.covenants import CovenantsCashServices, CovenantsDevicesServices
from src.types.covenants import (
    CovenantsCashRequest,
    CovenantsCashResponse,
    CovenantsDevicesRequest,
    CovenantsDevicesResponse,
)
from src.types.users import Login

covenants_cash_router = APIRouter(prefix="/covenants_cash", tags=["Covenants Cash"])

covenants_cash_services = CovenantsCashServices()


@covenants_cash_router.get("/", response_model=CovenantsCashResponse)
async def get_covenants_cash(
    current_user: Login = Depends(get_current_user),
) -> JSONResponse:
    content = covenants_cash_services.get_covenants_cash()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@covenants_cash_router.get(
    "/get_covenant_cash/{covenant_cash_id}", response_model=CovenantsCashResponse
)
async def get_covenant_cash(
    covenant_cash_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = covenants_cash_services.get_covenant_cash(
        covenant_cash_id=covenant_cash_id
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@covenants_cash_router.get(
    "/get_covenant_cash_by_name/{covenant_cash_name}",
    response_model=CovenantsCashResponse,
)
async def get_covenant_cash_by_name(
    covenant_cash_name: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = covenants_cash_services.get_covenant_cash_by_name(
        covenant_cash_name=covenant_cash_name
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@covenants_cash_router.post("/", response_model=CovenantsCashResponse)
async def insert_covenant_cash(
    covenants_cash_req: CovenantsCashRequest,
    current_user: Login = Depends(get_current_user),
) -> JSONResponse:
    content = covenants_cash_services.insert_covenant_cash(
        covenants_cash_req=covenants_cash_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@covenants_cash_router.delete(
    "/{covenant_cash_id}", response_model=CovenantsCashResponse
)
async def delete_covenant_cash(
    covenant_cash_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = covenants_cash_services.delete_covenant_cash(
        covenant_cash_id=covenant_cash_id
    )
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@covenants_cash_router.put("/{covenant_cash_id}", response_model=CovenantsCashResponse)
async def update_covenant_cash(
    covenant_cash_id: UUID,
    covenants_cash_req: CovenantsCashRequest,
    current_user: Login = Depends(get_current_user),
):
    content = covenants_cash_services.update_covenant_cash(
        covenant_cash_id=covenant_cash_id, covenants_cash_req=covenants_cash_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@covenants_cash_router.patch(
    "/{covenant_cash_id}", response_model=CovenantsCashResponse
)
async def update(
    covenant_cash_id: UUID,
    covenants_cash_req: CovenantsCashRequest,
    current_user: Login = Depends(get_current_user),
):
    content = covenants_cash_services.update_covenant_cash(
        covenant_cash_id=covenant_cash_id, covenants_cash_req=covenants_cash_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


covenants_devices_router = APIRouter(
    prefix="/covenants_device", tags=["Covenants Device"]
)

covenants_devices_services = CovenantsDevicesServices()


@covenants_devices_router.get("/", response_model=CovenantsDevicesResponse)
async def get_covenants_devices(
    current_user: Login = Depends(get_current_user),
) -> JSONResponse:
    content = covenants_devices_services.get_covenants_devices()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@covenants_devices_router.get(
    "/get_covenant_device/{covenant_device_id}", response_model=CovenantsDevicesResponse
)
async def get_covenant_device(
    covenant_device_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = covenants_devices_services.get_covenant_device(
        covenant_device_id=covenant_device_id
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@covenants_devices_router.get(
    "/get_covenant_device_by_name/{covenant_device_name}",
    response_model=CovenantsDevicesResponse,
)
async def get_covenant_device_by_name(
    covenant_device_name: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = covenants_devices_services.get_covenant_device_by_name(
        covenant_device_name=covenant_device_name
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@covenants_devices_router.post("/", response_model=CovenantsDevicesResponse)
async def insert_covenant_device(
    covenants_devices_req: CovenantsDevicesRequest,
    current_user: Login = Depends(get_current_user),
) -> JSONResponse:
    content = covenants_devices_services.insert_covenant_device(
        covenants_devices_req=covenants_devices_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@covenants_devices_router.delete(
    "/{covenant_device_id}", response_model=CovenantsDevicesResponse
)
async def delete_covenant_device(
    covenant_device_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = covenants_devices_services.delete_covenant_device(
        covenant_device_id=covenant_device_id
    )
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@covenants_devices_router.put(
    "/{covenant_device_id}", response_model=CovenantsDevicesResponse
)
async def update_covenant_device(
    covenant_device_id: UUID,
    covenants_devices_req: CovenantsDevicesRequest,
    current_user: Login = Depends(get_current_user),
):
    content = covenants_devices_services.update_covenant_device(
        covenant_device_id=covenant_device_id,
        covenants_devices_req=covenants_devices_req,
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@covenants_devices_router.patch(
    "/{covenant_device_id}", response_model=CovenantsDevicesResponse
)
async def update_device(
    covenant_device_id: UUID,
    covenants_devices_req: CovenantsDevicesRequest,
    current_user: Login = Depends(get_current_user),
):
    content = covenants_devices_services.update_device(
        covenant_device_id=covenant_device_id,
        covenants_devices_req=covenants_devices_req,
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )
