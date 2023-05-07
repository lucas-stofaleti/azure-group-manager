from fastapi.testclient import TestClient

from app.main import app
# from app.utils.config import settings

# settings.tenant_id = '123'

client = TestClient(app)
# settings.tenant_id = '123'


def test_read_main():
    response = client.get("/")
    assert response.status_code == 401