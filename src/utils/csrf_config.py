from fastapi import HTTPException, Request, status
from fastapi_csrf_protect import CsrfProtect
from pydantic import BaseModel

from src.utils.config import SECRET_KEY


class CsrfSettings(BaseModel):
    secret_key: str = SECRET_KEY


def check_csrf_protect(request: Request, csrf_protect: CsrfProtect):
    try:
        csrf_token = csrf_protect.get_csrf_from_headers(request.headers)
        csrf_protect.validate_csrf(csrf_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid CSRF token"
        )
