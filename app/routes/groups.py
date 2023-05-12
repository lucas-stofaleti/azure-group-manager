from typing import Union
from fastapi import APIRouter, Request, Depends, Header, Form, status
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
    return templates.TemplateResponse(
            "pages/group.html", {"request": request, "group": group}
    )

@group_router.post("/{id}")
@requires_auth
def group_post(request: Request, id: str, motivation: str = Form(...), mode: str = Form(...), db = Depends(get_connection)):
    group = get_group(db, id=id)
    user = get_token_claims(request)["oid"]
    if mode == "request-access":
        response = request_access(group=group, group_id=id, user=user, db=db, request=request, motivation=motivation)
    
    return response

### GROUP POST UTILS ###
def request_access(group, group_id: str, user: str, db, request: Request, motivation: str):
    requests = list(get_request(db=db, group_id=group_id, user=user))
    has_request = [element["status"] for element in requests]
    print(has_request)
    if has_request and ("Approved" in has_request or "Waiting approval" in has_request):
        err = f"User already requested access to this group."
        response = templates.TemplateResponse(
            "pages/group.html", {"request": request, "group": group, "error": err}
        )
        response.status_code = status.HTTP_409_CONFLICT
        return response
    group_request = create_request(db=db, motivation=motivation, id=group_id, user=user)
    msg = f"Request created: {group_request.inserted_id}"
    response = templates.TemplateResponse(
        "pages/group.html", {"request": request, "group": group, "msg": msg}
    )
    response.status_code = status.HTTP_201_CREATED
    return response