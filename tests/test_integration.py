def test_healthcheck(client_app):
    response = client_app.get("/")
    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "OK"

def test_pokedex(client_app):
    response = client_app.get("/pokedex?limit=151")
    assert response.status_code == 200
    res = response.json()
    assert len(res) == 151
