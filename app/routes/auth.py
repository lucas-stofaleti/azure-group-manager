from fastapi import APIRouter, Request
from typing import Union
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.utils.identity import msal_client
from app.utils.config import settings
import json

templates = Jinja2Templates(directory="app/templates")

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@auth_router.get("/login")
def login(request: Request, msg: Union[int, None] = None, error: Union[int, None] = None):
    client = msal_client.initiate_auth_code_flow(scopes=[settings.scope], redirect_uri=f"{settings.domain}/auth/callback")
    url = client["auth_uri"]

    response = templates.TemplateResponse(
        "pages/login.html", {"request": request, "url": url, "msg": msg, "error": error}
    )
    response.set_cookie(key="code_flow", value=client, httponly=True)
    return response

@auth_router.get("/callback")
def callback(request: Request, code: str, client_info: str, state: str, session_state: str):
    auth_code_flow = request.cookies.get("code_flow", None).replace("'", '"').replace("None", "null")
    auth_code_flow = json.loads(auth_code_flow)
    auth_response = {
        "code": code,
        "client_info": client_info,
        "state": state,
        "session_state": session_state
    }
    msal_response = msal_client.acquire_token_by_auth_code_flow(auth_code_flow=auth_code_flow, auth_response=auth_response, scopes=[settings.scope])
    token = f'Bearer {msal_response["access_token"]}'
    response = RedirectResponse(f"/", status_code=303)
    response.set_cookie(key="token", value=token, httponly=True)
    response.set_cookie(key="code_flow", value="", httponly=True, expires=0)
    return response

@auth_router.get("/logout")
def logout():
    response = RedirectResponse(f"/auth/login", status_code=303)
    response.set_cookie(key="token", value="", httponly=True, expires=0)
    return response