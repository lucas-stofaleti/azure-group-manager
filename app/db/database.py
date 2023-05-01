import pymongo
from app.utils.config import settings

client = pymongo.MongoClient(f"mongodb+srv://{settings.mongo_user}:{settings.mongo_password}@{settings.mongo_url}/?retryWrites=true&w=majority")
db = client.group_manager

def get_connection():
    return db
