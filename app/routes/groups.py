from typing import Union
from fastapi import APIRouter, Request, Depends, Header
from fastapi.templating import Jinja2Templates
from app.utils.identity import *
from app.db.database import get_connection
from app.db.crud import *

templates = Jinja2Templates(directory="app/templates")

group_router = APIRouter(
    prefix="/groups",
    tags=["groups"],
)

@group_router.get("/")
@requires_auth
def groups(request: Request, db = Depends(get_connection), membership: str = "all"):
    if not request.headers.get('HX-Request'):
        return templates.TemplateResponse(
            "pages/groups.html", {"request": request}
        )
    user = get_token_claims(request)["oid"]
    groups = list(get_groups(db, user=user, membership=membership))
    return templates.TemplateResponse(
        "partials/group_table.html", {"request": request, "groups": groups}
    )

@group_router.get("/{id}")
@requires_auth
def group(request: Request, id: str, db = Depends(get_connection)):
    group = get_group(db, id=id)
    print(group)
    return templates.TemplateResponse(
            "pages/group.html", {"request": request, "group": group}
    )