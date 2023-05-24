from fastapi import APIRouter, Request, Depends, Form, status, Cookie
from fastapi.templating import Jinja2Templates
from app.utils.identity import *
from app.db.database import get_connection
from app.db.crud import *
from app.utils.graph import list_group_members, create_group_graph, get_graph_user

templates = Jinja2Templates(directory="app/templates")

request_router = APIRouter(
    prefix="/requests",
    tags=["requests"],
)

@request_router.get("/")
@requires_auth
def request(request: Request):
    if not request.headers.get('HX-Request'):
        return templates.TemplateResponse(
            "pages/requests.html", {"request": request}
        )
    
