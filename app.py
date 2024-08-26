from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from sqlalchemy.exc import IntegrityError

from src.utils.app_config import setup_middleware
from src.utils.app_routers import setup_routers
from src.utils.csrf_config import CsrfSettings

app = FastAPI(
    title="Project Management API ",
    version="1.0",
    description="This API will contains All tools for you to Management Project ",
)

setup_middleware(app)
setup_routers(app)


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


ERROR_MESSAGES = {
    status.HTTP_422_UNPROCESSABLE_ENTITY: "Not Exist",
    status.HTTP_404_NOT_FOUND: "Not Found",
    status.HTTP_401_UNAUTHORIZED: "User Not UNAUTHORIZED",
    status.HTTP_409_CONFLICT: "Can't Proceed Your Request",
    status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
    status.HTTP_502_BAD_GATEWAY: "Bad Gateway Try Again Later",
    status.HTTP_403_FORBIDDEN: "Invalid CSRF token",
    status.HTTP_406_NOT_ACCEPTABLE: "Violates Constraint",
}


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    status_code = exc.status_code
    message = ERROR_MESSAGES.get(status_code, exc.detail)

    content = {"message": message, "error": str(exc)}

    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))


@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    status_code = exc.status_code
    message = ERROR_MESSAGES.get(status_code, exc.detail)

    content = {"message": message, "error": str(exc)}

    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
