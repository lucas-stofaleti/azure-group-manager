import pymongo
import logging
from app.utils.config import settings

logger = logging.getLogger(__name__)

class DataBase:
    client: pymongo.MongoClient = None

db = DataBase()

def connect_to_mongo():
    logger.info('Initializing Mongo Client...')
    db.client = pymongo.MongoClient(f"mongodb+srv://{settings.mongo_user}:{settings.mongo_password}@{settings.mongo_url}/?retryWrites=true&w=majority")
    check_db()
    logger.info('Connected to Mongo DB!')

def close_mongo_connection():
    logger.info('Closing Mongo Client...')
    db.client.close()
    logger.info('Connection to MongoDB closed!')

def check_db():
    logger.info("Testing connection to MongoDB...")
    db.client.admin.command('ping')
    logger.info("Connection to MongoDB successfully established!")

def get_connection():
    return db.client.group_manager
