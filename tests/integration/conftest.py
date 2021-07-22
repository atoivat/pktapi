import pytest

from core.schemas.Trainer import Trainer


@pytest.fixture
def trainer_data(db):
    trainer = {
        "name": "Test",
        "username": "test",
        "password": "1234"
    }
    yield trainer
    db.query(Trainer)\
        .filter(Trainer.username == trainer["username"])\
        .delete()
    db.commit()


@pytest.fixture
def trainer(client_app, trainer_data):
    response = client_app.post("/trainers/", json=trainer_data)
    return response.json()


@pytest.fixture
def alt_trainer(client_app, db):
    trainer_data = {
        "name": "Test2",
        "username": "test2",
        "password": "1234"
    }
    response = client_app.post("/trainers/", json=trainer_data)
    trainer = response.json()
    yield trainer
    db.query(Trainer)\
        .filter(Trainer.id == trainer["id"])\
        .delete()
    db.commit()


@pytest.fixture
def token(client_app, trainer):
    data = {"username": trainer["username"], "password": "1234"}
    response = client_app.post("/token", data=data)
    return response.json()


@pytest.fixture
def header(token):
    access_token = token["access_token"]
    header = {
        "Authorization": f"Bearer {access_token}"
    }
    return header
