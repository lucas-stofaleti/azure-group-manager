from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.utils.identity import requires_auth

templates = Jinja2Templates(directory="app/templates")

group_router = APIRouter(
    prefix="/groups",
    tags=["groups"],
)

@group_router.get("/")
@requires_auth
def groups(request: Request):
    return templates.TemplateResponse(
        "pages/groups.html", {"request": request}
    )