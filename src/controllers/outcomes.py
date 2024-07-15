from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.oauth2 import get_current_user
from src.services.outcomes import OutcomesServices
from src.types.outcomes import OutcomesRequest, OutcomesResponse
from src.types.users import Login

outcomes_router = APIRouter(prefix="/outcomes", tags=["Outcomes"])
outcomes_services = OutcomesServices()


@outcomes_router.get("/", response_model=OutcomesResponse)
async def get_outcomes(current_user: Login = Depends(get_current_user)) -> JSONResponse:
    content = outcomes_services.get_outcomes()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@outcomes_router.get("/get_outcome/{outcome_id}", response_model=OutcomesResponse)
async def get_outcome(
    outcome_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = outcomes_services.get_outcome(outcome_id=outcome_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@outcomes_router.get(
    "/get_outcome_by_buyer_name/{outcome_buyer_name}", response_model=OutcomesResponse
)
async def get_outcome_by_buyer_name(
    outcome_buyer_name: str, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = outcomes_services.get_outcome_by_buyer_name(
        outcome_buyer_name=outcome_buyer_name
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@outcomes_router.get(
    "/get_outcome_by_amount_payed/{outcome_amount_payed}",
    response_model=OutcomesResponse,
)
async def get_outcome_by_amount_payed(
    outcome_amount_payed: float, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = outcomes_services.get_outcome_by_amount_payed(
        outcome_amount_payed=outcome_amount_payed
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@outcomes_router.get(
    "/get_outcome_by_date/{outcome_date}", response_model=OutcomesResponse
)
async def get_outcome_by_date(
    outcome_date: datetime, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = outcomes_services.get_outcome_by_date(outcome_date=outcome_date)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@outcomes_router.post("/", response_model=OutcomesResponse)
async def insert_outcome(
    outcomes_req: OutcomesRequest, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = outcomes_services.insert_outcome(outcomes_req=outcomes_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@outcomes_router.delete("/{outcome_id}", response_model=OutcomesResponse)
async def delete_outcome(
    outcome_id: UUID, current_user: Login = Depends(get_current_user)
) -> JSONResponse:
    content = outcomes_services.delete_outcome(outcome_id=outcome_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=content,
    )


@outcomes_router.put("/{outcome_id}", response_model=OutcomesResponse)
async def update_outcome(
    outcome_id: UUID,
    outcomes_req: OutcomesRequest,
    current_user: Login = Depends(get_current_user),
):
    content = outcomes_services.update_outcome(
        outcome_id=outcome_id, outcomes_req=outcomes_req
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )


@outcomes_router.patch("/{outcome_id}", response_model=OutcomesResponse)
async def update(
    outcome_id: UUID,
    outcomes_req: OutcomesRequest,
    current_user: Login = Depends(get_current_user),
):
    content = outcomes_services.update(outcome_id=outcome_id, outcomes_req=outcomes_req)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=content,
    )
