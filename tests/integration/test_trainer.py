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


def test_get_current_trainer(client_app, header):
    response = client_app.get("/trainers/me", headers=header)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "Test"
    assert response_json["username"] == "test"


def test_update_trainer(client_app, header):
    # Check before update
    response = client_app.get("/trainers/test")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "Test"
    assert response_json["username"] == "test"

    # Update
    new_data = {
        "name": "TestUpdate",
        "username": "testupdate"
    }
    response = client_app.put("/trainers/me", json=new_data, headers=header)
    assert response.status_code == 200

    # Check update
    response = client_app.get("/trainers/testupdate")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "TestUpdate"
    assert response_json["username"] == "testupdate"

    # Revert update
    token_response = client_app.post(
        "/token", data={"username": "testupdate", "password": 1234}
    )
    access_token = token_response.json()["access_token"]
    header = {
        "Authorization": f"Bearer {access_token}"
    }
    new_data = {
        "user": "Test",
        "username": "test"
    }
    response = client_app.put("/trainers/me", json=new_data, headers=header)
    assert response.status_code == 200


def test_update_username_already_exists(client_app, header, alt_trainer):
    new_data = {
        "username": "test2"
    }
    response = client_app.put("/trainers/me", json=new_data, headers=header)
    assert response.status_code == 400


def test_delete_trainer(client_app, header):
    response = client_app.get("/trainers/test")
    assert response.status_code == 200

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
