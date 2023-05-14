from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.utils.identity import requires_auth
import logging

logger = logging.getLogger(__file__)

templates = Jinja2Templates(directory="app/templates")

home_router = APIRouter(
    tags=["home"],
)

@home_router.get("/")
@requires_auth
def home(request: Request):
    logger.info('Home executed')
    return templates.TemplateResponse(
        "pages/home.html", {"request": request}
    )