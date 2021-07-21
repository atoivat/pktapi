def test_healthcheck(client_app):
    response = client_app.get("/")
    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "OK"

def test_token(client_app, trainer):
    data = {"username": trainer["username"], "password": "1234"}
    response = client_app.post("/token", data=data)
    assert response.status_code == 200
    response_json = response.json()
    assert type(response_json["access_token"]) is str
    assert type(response_json["token_type"]) is str
