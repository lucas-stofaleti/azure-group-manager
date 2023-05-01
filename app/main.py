from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import *

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(auth_router)
app.include_router(home_router)
app.include_router(partials_router)