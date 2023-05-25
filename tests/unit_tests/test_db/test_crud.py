from datetime import datetime
from app.db.crud import get_requests_by_filter

date = datetime(2023, 5, 24, 14, 9, 55, 915000)

DUMMY_REQUESTS = [{
        "group_id": "c735c620-17a3-4b0b-bde9-c6a14a5a335f",
        "request_time": date,
        "user_id": "caf7fa2c-a2ca-4cef-84ac-2020c3fce0a1",
        "motivation": "My motivation",
        "status": "Waiting approval"
    },
    {
        "group_id": "d835c620-17a3-4b0b-bde9-c6a14a5a336g",
        "request_time": date,
        "user_id": "dbf7fa2c-a2ca-4cef-84ac-2020c3fce0b2",
        "motivation": "Other motivation",
        "status": "Waiting approval"
    },
    {
        "group_id": "d835c620-17a3-4b0b-bde9-c6a14a5a336g",
        "request_time": date,
        "user_id": "ecf7fa2c-a2ca-4cef-84ac-2020c3fce0c3",
        "motivation": "Other motivation",
        "status": "Approved"
    }
]

def feed_db_requests(db, collection: str, value: dict):
    request = db[collection].insert_many(value)

def test_get_requests_by_filter(db):
    feed_db_requests(db=db, collection="requests", value=DUMMY_REQUESTS)
    # Read all requests, no filter
    requests = list(get_requests_by_filter(db=db, filter={}))
    assert len(requests) == len(DUMMY_REQUESTS), f"Size of Dummy ({len(DUMMY_REQUESTS)}) should be equal of size of response ({len(requests)})"
    # Filter first request
    requests = list(get_requests_by_filter(db=db, filter=DUMMY_REQUESTS[0]))
    assert requests == [DUMMY_REQUESTS[0]]
    # Filter by group
    requests = list(get_requests_by_filter(db=db, filter={"group_id": DUMMY_REQUESTS[1]["group_id"]}))
    assert DUMMY_REQUESTS[1] in requests