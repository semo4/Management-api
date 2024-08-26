from fastapi import FastAPI, Request, status
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
