from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_connection():
    assert client.get("/").status_code == 200
