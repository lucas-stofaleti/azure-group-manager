from bson import ObjectId

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