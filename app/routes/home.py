from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

home_router = APIRouter(
    tags=["home"],
)

@home_router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "pages/login.html", {"request": request}
    )