def test_get_pokemons(client_app, pokemon_in_db):
    response = client_app.get("/pokemons")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]["data"]["id"] == 1


def test_create_pokemon(client_app, header, pokemon_data):
    response = client_app.post(
        "/pokemons/", json=pokemon_data, headers=header
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["level"] == 1
    assert response_json.get("nickname") is None
    assert type(response_json["data"]) is dict
    assert response_json["data"]["name"] == "Bulbasaur"


def test_create_pokemon_with_nickname(client_app, header, pokemon_data):
    pokemon_data["nickname"] = "Bulby"
    response = client_app.post(
        "/pokemons/", json=pokemon_data, headers=header
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["level"] == 1
    assert response_json["nickname"] == "Bulby"
    assert type(response_json["data"]) is dict
    assert response_json["data"]["name"] == "Bulbasaur"


def test_create_pokemon_invalid_data_id(client_app, header, pokemon_data):
    pokemon_data["data_id"] = 600000
    response = client_app.post(
        "/pokemons/", json=pokemon_data, headers=header
    )
    assert response.status_code == 400
