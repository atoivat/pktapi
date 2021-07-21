def test_get_trainers(client_app, trainer):
    response = client_app.get("/trainers")
    assert response.status_code == 200
    response_json = response.json()
    assert type(response_json) is list
    assert response_json[0]["name"] == "Test"
    assert response_json[0]["username"] == "test"


def test_create(client_app, trainer_data):
    response = client_app.post("/trainers/", json=trainer_data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] is not None
    assert response_json["name"] == "Test"
    assert response_json["username"] == "test"
    assert type(response_json["team"]) is list


def test_create_empty(client_app):
    trainer_data = {
        "name": "   ",
        "username": "   ",
        "password": "   "
    }
    response = client_app.post("/trainers/", json=trainer_data)
    assert response.status_code == 400


def test_create_same_username(client_app, trainer, trainer_data):
    response = client_app.post("/trainers/", json=trainer_data)
    assert response.status_code == 400


def test_get_current_trainer(client_app, token):
    access_token = token["access_token"]
    header = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client_app.get("/trainers/me", headers=header)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "Test"
    assert response_json["username"] == "test"


def test_delete_trainer(client_app, token):
    response = client_app.get("/trainers/test")
    assert response.status_code == 200

    access_token = token["access_token"]
    header = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client_app.delete("/trainers/me", headers=header)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "Test"
    assert response_json["username"] == "test"
    
    response = client_app.get("/trainers/test")
    assert response.status_code == 404



def test_get_trainer(client_app, trainer):
    response = client_app.get("/trainers/test")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "Test"
    assert response_json["username"] == "test"


def test_get_trainer_not_found(client_app):
    response = client_app.get("/trainers/test")
    assert response.status_code == 404
