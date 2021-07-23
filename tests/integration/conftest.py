import pytest

from core.schemas.Trainer import Trainer
from core.schemas.Pokemon import Pokemon


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


@pytest.fixture
def alt_header(client_app, alt_trainer):
    data = {"username": alt_trainer["username"], "password": "1234"}
    response = client_app.post("/token", data=data)
    token = response.json()
    access_token = token["access_token"]
    header = {
        "Authorization": f"Bearer {access_token}"
    }
    return header    


@pytest.fixture
def pokemon_data(db):
    pokemon = {
        "data_id": 1,
        "level": 1
    }
    yield pokemon
    db.query(Pokemon)\
        .filter(Pokemon.data_id == 1)\
        .delete()
    db.commit()


@pytest.fixture
def pokemon_in_db(db, client_app, header, pokemon_data):
    response = client_app.post(
        "/pokemons/", json=pokemon_data, headers=header
    )
    return response.json()