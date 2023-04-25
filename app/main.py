from fastapi import FastAPI
from app.routes import *

app = FastAPI()
app.include_router(auth_router)
