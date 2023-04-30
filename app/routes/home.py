from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.utils.identity import requires_auth

templates = Jinja2Templates(directory="app/templates")

home_router = APIRouter(
    tags=["home"],
)

@home_router.get("/list_groups")
@requires_auth
def clicked(request: Request):
    groups = [
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA). Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        },
        {
            "id": "#001",
            "name": "nice-group",
            "description": "Members of team Discovery (SSA).",
            "members": "15",
            "admins": "2"
        }
    ]
    return templates.TemplateResponse(
        "partials/group_table.html", {"request": request, "groups": groups}
    )

@home_router.post("/filter")
async def filter(request: Request):
    form = await request.form()
    print(form)
    return templates.TemplateResponse(
        "pages/groups.html", {"request": request}
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