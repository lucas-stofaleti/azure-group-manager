from fastapi.testclient import TestClient
from app.main import app
from app.routes.requests import *

TOKEN = ""

client = TestClient(app, cookies={
    "token": TOKEN
})

# def test_requests_home(mocker):
#     # mocker.patch(
#     #     'app.utils.identity.requires_auth',
#     #     return_value = "123"
#     # )
#     response = client.get("/requests")
#     print(response.text)
#     assert response.status_code == 200
#     assert response.json() == TOKEN
