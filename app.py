from fastapi import FastAPI, HTTPException, Request
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from sqlalchemy.exc import IntegrityError

from src.utils.app_config import build_exception_response, setup_middleware
from src.utils.app_routers import setup_routers
from src.utils.csrf_config import CsrfSettings

app = FastAPI(
    title="Project Management API ",
    version="1.0",
    description="This API will contains All tools for you to Management Project",
)

setup_middleware(app)
setup_routers(app)


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return build_exception_response(exc)


@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    return build_exception_response(exc)


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return build_exception_response(exc)
