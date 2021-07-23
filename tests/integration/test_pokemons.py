def test_get_pokemons(client_app, pokemon_in_db):
    response = client_app.get("/pokemons")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]["data"]["id"] == 1
    assert response_json[0]["trainer"] == "test"


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


def test_get_pokemon(client_app, header, pokemon_in_db):
    poke_id = pokemon_in_db["id"]
    response = client_app.get(f"/pokemons/{poke_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["trainer"] == "test"
    assert type(response_json["data"]) is dict;
    assert response_json["data"]["id"] == 1


def test_get_pokemon_not_found(client_app, header):
    poke_id = -1
    response = client_app.get(f"/pokemons/{poke_id}")
    assert response.status_code == 404


def test_update_pokemon(client_app, header, pokemon_in_db):
    # Check before update
    poke_id = pokemon_in_db["id"]
    response = client_app.get(f"/pokemons/{poke_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["nickname"] is None
    assert response_json["level"] == 1
    assert response_json["id"] == poke_id

    # Update
    new_data = {
        "nickname": "Bulby",
        "level": 2
    }
    response = client_app.put(
        f"/pokemons/{poke_id}", json=new_data, headers=header
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["nickname"] == "Bulby"
    assert response_json["level"] == 2
    assert response_json["id"] == poke_id


def test_update_pokemon_nickname(client_app, header, pokemon_in_db):
    poke_id = pokemon_in_db["id"]
    
    new_data = {
        "nickname": "Bulby",
        "level": 2
    }
    response = client_app.put(
        f"/pokemons/{poke_id}", json=new_data, headers=header
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["nickname"] == "Bulby"
    assert response_json["level"] == 2
    assert response_json["id"] == poke_id


    new_data = {
        "nickname": ""
    }
    response = client_app.put(
        f"/pokemons/{poke_id}", json=new_data, headers=header
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["nickname"] is None
    assert response_json["level"] == 2
    assert response_json["id"] == poke_id


def test_update_not_found(client_app, header):
    new_data = {
        "nickname": ""
    }
    response = client_app.put(
        f"/pokemons/{-1}", json=new_data, headers=header
    )
    assert response.status_code == 404


def test_update_forbidden(client_app, alt_header, pokemon_in_db):
    poke_id = pokemon_in_db["id"]
    
    new_data = {
        "level": 2
    }
    response = client_app.put(
        f"/pokemons/{poke_id}", json=new_data, headers=alt_header
    )
    assert response.status_code == 403


def test_delete(client_app, header, pokemon_in_db):
    poke_id = pokemon_in_db["id"]
    response = client_app.delete(f"/pokemons/{poke_id}", headers=header)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == poke_id

    response = client_app.get(f"/pokemons/{poke_id}")
    assert response.status_code == 404


def test_delete_not_found(client_app, header):
    response = client_app.delete(f"/pokemons/{-1}", headers=header)
    assert response.status_code == 404


def test_delete_forbidden(client_app, alt_header, pokemon_in_db):
    poke_id = pokemon_in_db["id"]
    response = client_app.delete(f"/pokemons/{poke_id}", headers=alt_header)
    assert response.status_code == 403
