from bson import ObjectId
from datetime import datetime

def get_groups(db, user: str, membership: str = "all"):
    query = {}
    if membership == "member":
        query = {
            "members": user
        }
    elif membership == "no-access":
        query = {
            "members": {"$ne": user}
        }
    elif membership == "admin":
        query = {
            "admins": user
        }
    groups = db.groups.find(query)
    return groups

def get_group(db, id: str):
    group = db.groups.find_one({"_id": ObjectId(id)})
    return group

def create_request(db, motivation: str, id: str, user: str):
    now = datetime.now()
    request = db.requests.insert_one({
        "group_id": ObjectId(id),
        "request_time": now,
        "user_id": user,
        "motivation": motivation,
        "status": "Waiting approval"
    })
    return request

def get_requests(db, group_id: str, user: str, status = None):
    if status:
        request = db.requests.find({
            "group_id": ObjectId(group_id),
            "user_id": user,
            "status": status
        })
    else:
        request = db.requests.find({
            "group_id": ObjectId(group_id),
            "user_id": user
        })
    return request