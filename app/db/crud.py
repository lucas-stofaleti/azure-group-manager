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
    group = db.groups.find_one({"_id": id})
    return group

def get_group_by_name(db, name: str):
    group = db.groups.find_one({"name": name})
    return group

def create_request(db, motivation: str, id: str, user: str):
    now = datetime.now()
    request = db.requests.insert_one({
        "group_id": id,
        "request_time": now,
        "user_id": user,
        "motivation": motivation,
        "status": "Waiting approval"
    })
    return request

def create_group_db(db, description: str, user_id: str, name: str, group_id: str):
    now = datetime.now()
    request = db.groups.insert_one({
        "_id": group_id,
        "name": name,
        "creation_time": now,
        "members": [user_id],
        "owners": [user_id],
        "description": description,
        "is_active": True
    })
    return request


def get_requests(db, group_id: str, user: str, status = None):
    if status:
        request = db.requests.find({
            "group_id": group_id,
            "user_id": user,
            "status": status
        })
    else:
        request = db.requests.find({
            "group_id": group_id,
            "user_id": user
        })
    return request