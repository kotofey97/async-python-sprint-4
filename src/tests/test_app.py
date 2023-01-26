from http import HTTPStatus
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_db_status():
    response = client.get('/api/v1/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'version': 'v1'}