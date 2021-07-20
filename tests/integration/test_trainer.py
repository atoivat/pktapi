def test_get_trainers(client_app, trainer):
    response = client_app.get("/trainers")
    assert response.status_code == 200
    response_json = response.json()
    assert type(response_json) is list
    assert response_json[0]["name"] == "Test"
    assert response_json[0]["username"] == "test"


def test_create(client_app, trainer_data):
    response = client_app.post("/trainers/create", json=trainer_data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] is not None
    assert response_json["name"] == "Test"
    assert response_json["username"] == "test"
    assert type(response_json["team"]) is list


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