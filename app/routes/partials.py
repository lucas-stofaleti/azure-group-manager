from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.utils.identity import requires_auth
from app.db.database import get_connection
from app.db.crud import *

templates = Jinja2Templates(directory="app/templates")

partials_router = APIRouter(
    prefix="/partials",
    tags=["partials"],
)

@partials_router.get("/groups")
@requires_auth
def groups(request: Request, db = Depends(get_connection), membership: str = "all"):
    groups = list(get_groups(db))
    print(groups)
    return templates.TemplateResponse(
        "partials/group_table.html", {"request": request, "groups": groups}
    )
