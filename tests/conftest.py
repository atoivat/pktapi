import pytest
from fastapi.testclient import TestClient

from app.main import app

@pytest.fixture
def client_app():
    client = TestClient(app)
    return client