from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware

# from src.services.authentication import AuthServices
from src.utils.config import SECRET_KEY


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Strict-Transport-Security"] = (
            "max-age=3600; includeSubDomains"
        )
        return response


class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ["GET", "POST", "PUT", "DELETE"]:  # Add GET if needed
            csrf_token = request.headers.get("X-CSRF-Token")
            csrf_protect = CsrfProtect()
            try:
                await csrf_protect.validate_csrf(csrf_token)
            except Exception:
                return JSONResponse(
                    {"error": "Invalid CSRF token"},
                    status_code=status.HTTP_403_FORBIDDEN,
                )
        response = await call_next(request)
        return response


def setup_middleware(app: FastAPI):
    origins = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(SecurityHeadersMiddleware)
    # app.add_middleware(CSRFMiddleware)
    app.add_middleware(
        SessionMiddleware,
        secret_key=SECRET_KEY,
        max_age=3600,
        same_site="lax",
    )


def build_exception_response(exc):
    ERROR_MESSAGES = {
        status.HTTP_422_UNPROCESSABLE_ENTITY: "Not Exist",
        status.HTTP_404_NOT_FOUND: "Not Found",
        status.HTTP_401_UNAUTHORIZED: "User UNAUTHORIZED",
        status.HTTP_409_CONFLICT: "Can't Proceed Your Request",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        status.HTTP_502_BAD_GATEWAY: "Bad Gateway Try Again Later",
        status.HTTP_403_FORBIDDEN: "Invalid CSRF token",
        status.HTTP_406_NOT_ACCEPTABLE: "Violates Constraint",
    }

    status_code = exc.status_code
    message = ERROR_MESSAGES.get(status_code, exc.detail)

    content = {"message": message, "detail": str(exc)}
    JSONResponse(status_code=status_code, content=jsonable_encoder(content))
