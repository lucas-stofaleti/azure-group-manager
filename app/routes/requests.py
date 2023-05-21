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
    # user = get_graph_user("123")
    auth = request.cookies.get("token", None)
    return auth
