from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.utils.identity import requires_auth

templates = Jinja2Templates(directory="app/templates")

home_router = APIRouter(
    tags=["home"],
)


@home_router.get("/groups")
@requires_auth
def groups(request: Request):
    return templates.TemplateResponse(
        "pages/groups.html", {"request": request}
    )

@home_router.get("/")
@requires_auth
def home(request: Request):
    return templates.TemplateResponse(
        "pages/home.html", {"request": request}
    )

@home_router.get("/test")
@requires_auth
def test(request: Request):
    return templates.TemplateResponse(
        "pages/test.html", {"request": request}
    )