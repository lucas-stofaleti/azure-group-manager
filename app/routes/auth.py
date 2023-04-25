from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@auth_router.get("/")
def login(request: Request):
    return templates.TemplateResponse(
        "pages/login.html", {"request": request}
    )