import pytest
import mongomock

@pytest.fixture
def db():
    mongo = mongomock.MongoClient()
    db = mongo.get_database("group_manager")
    return db