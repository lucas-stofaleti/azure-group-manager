from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import msal

templates = Jinja2Templates(directory="app/templates")

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

value = msal.ConfidentialClientApplication(
        "", authority="https://login.microsoftonline.com/",
        client_credential="")

@auth_router.get("/login")
def login(request: Request):
    url = value.get_authorization_request_url(scopes=[], redirect_uri="http://localhost:8000/auth/callback")
    return templates.TemplateResponse(
        "pages/login.html", {"request": request, "url": url}
    )

@auth_router.post("/login")
def login_post(request: Request):
    value = msal.ConfidentialClientApplication(
        "b52287e5-8650-43dd-b760-498810711076", authority="https://login.microsoftonline.com/c56c9508-ff89-4cd0-95f4-aa3ec7fb056f",
        client_credential="Pxr8Q~PrAZpVNAEsa.qFudQ2lPvVpF~WXJMlVbje")
    url = value.get_authorization_request_url(scopes=[], redirect_uri="http://localhost:8000/auth/callback")
    return RedirectResponse(url)

@auth_router.get("/test")
def test(request: Request):
    value = msal.ConfidentialClientApplication(
        "b52287e5-8650-43dd-b760-498810711076", authority="https://login.microsoftonline.com/c56c9508-ff89-4cd0-95f4-aa3ec7fb056f",
        client_credential="Pxr8Q~PrAZpVNAEsa.qFudQ2lPvVpF~WXJMlVbje")
    url = value.get_authorization_request_url(scopes=[], redirect_uri="http://localhost:8000/auth/callback")
    print(url)
    return "ok"

@auth_router.get("/callback")
def callback(request: Request):
    
    return "callback"