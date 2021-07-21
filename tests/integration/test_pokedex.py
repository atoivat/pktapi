def test_pokedex(client_app):
    response = client_app.get("/pokedex")
    assert response.status_code == 200
    res = response.json()
    assert type(res) == list

def test_get_pokemon(client_app):
    response = client_app.get("/pokedex/1")
    assert response.status_code == 200
    res = response.json()
    assert res["id"] == 1
    assert res["name"] == "Bulbasaur"

def test_get_pokemon_not_found(client_app):
    response = client_app.get("/pokedex/-1")
    assert response.status_code == 404