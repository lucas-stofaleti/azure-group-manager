from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.utils.identity import msal_client
from app.utils.config import settings

templates = Jinja2Templates(directory="app/templates")

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@auth_router.get("/login")
def login(request: Request, msg: str | None = None, error: str | None = None):
    url = msal_client.get_authorization_request_url(scopes=[settings.scope], redirect_uri=f"{settings.domain}/auth/callback")
    return templates.TemplateResponse(
        "pages/login.html", {"request": request, "url": url, "msg": msg, "error": error}
    )

@auth_router.get("/callback")
def callback(code: str):
    token = f'Bearer {msal_client.acquire_token_by_authorization_code(code=code, scopes=[settings.scope], redirect_uri=f"{settings.domain}/auth/callback")["access_token"]}'
    response = RedirectResponse(f"/", status_code=303)
    response.set_cookie(key="token", value=token, httponly=True)
    return response