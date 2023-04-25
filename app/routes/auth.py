from fastapi import APIRouter

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@auth_router.get("/")
def login():
    return "hello world"