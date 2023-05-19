from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
import logging
from app.routes import *
from app.db.database import connect_to_mongo, close_mongo_connection
from app.utils.graph import check_graph_connection

logging.basicConfig(encoding='utf-8', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_mongo()
    check_graph_connection()
    yield
    close_mongo_connection()

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(auth_router)
app.include_router(home_router)
app.include_router(group_router)