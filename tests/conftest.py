from core.database import SessionLocal
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import engine

from app.main import app

@pytest.fixture
def client_app():
    client = TestClient(app)
    return client

@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    except:
        session.rollback()
    finally:
        session.close()
