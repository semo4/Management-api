from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

# from urllib.error import HTTPError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from src.controllers.authentication import auth_router
from src.controllers.bills import bills_router
from src.controllers.contractors import contractors_router
from src.controllers.covenants import covenants_cash_router, covenants_devices_router
from src.controllers.incomes import incomes_router
from src.controllers.operations import operations_router
from src.controllers.outcomes import outcomes_router
from src.controllers.outcomes_categories import categories_router
from src.controllers.partners import partners_router
from src.controllers.projects import projects_router
from src.controllers.salaries import salaries_router
from src.controllers.sections import section_router
from src.controllers.users import users_router
from src.controllers.withdraw import withdraw_router
from src.controllers.withdraw_contractors import withdraw_contractors_router
from src.controllers.workers import workers_router
from src.controllers.workplaces import workplace_router

app = FastAPI(
    title="Project Management API ",
    version="1.0",
    description="This API will contains All tools for you to Management Project ",
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(section_router)
app.include_router(workplace_router)
app.include_router(categories_router)
app.include_router(workers_router)
app.include_router(projects_router)
app.include_router(partners_router)
app.include_router(covenants_cash_router)
app.include_router(covenants_devices_router)
app.include_router(bills_router)
app.include_router(contractors_router)
app.include_router(incomes_router)
app.include_router(outcomes_router)
app.include_router(operations_router)
app.include_router(salaries_router)
app.include_router(withdraw_contractors_router)
app.include_router(withdraw_router)
app.include_router(users_router)
app.include_router(auth_router)


@app.exception_handler(HTTPException)
async def https_exception_handler(request, exc):
    if exc.status_code == 422:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"message": "Not Exist", "error": str(exc)}),
        )
    if exc.status_code == 401:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder(
                {"message": "User Not UNAUTHORIZED", "error": str(exc)}
            ),
        )
    if exc.status_code == 404:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder(
                {"message": exc.detail, "error": str(exc)}
            ),
        )
    if exc.status_code == 409:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=jsonable_encoder(
                {"message": "Can't Proceed Your Request", "error": str(exc)}
            ),
        )
    if exc.status_code == 500:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(
                {"message": "Internal Server Error", "error": str(exc)}
            ),
        )

    if exc.status_code == 502:
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=jsonable_encoder(
                {"message": "Bad Gateway Try Again Later", "error": str(exc)}
            ),
        )


@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        content=jsonable_encoder({"message": "violates constraint", "error": str(exc)}),
    )
