def user(client, name):
    response = client.post("/users", json={"name": name})
    assert response.status_code == 201
    return response.json()["id"]


def test_team_notes(client):
    alice = user(client, "Alice")
    bob = user(client, "Bob")
    team = client.post("/teams", headers={"x-user-id": alice}, json={"name": "Engineering"}).json()["id"]
    url = f"/teams/{team}/notes"
    headers = {"x-user-id": alice}
    created = client.post(url, headers=headers, json={"title": "Plan", "content": "First draft"})
    assert created.status_code == 201
    note_id = created.json()["id"]
    assert client.get(url, headers={"x-user-id": bob}).status_code == 403
    assert client.post(f"/teams/{team}/members/{bob}", headers=headers).status_code == 204
    assert len(client.get(url, headers={"x-user-id": bob}).json()) == 1
    assert client.patch(f"{url}/{note_id}", headers={"x-user-id": bob}, json={"content": "Updated"}).json()["content"] == "Updated"
    assert client.get(f"{url}/{note_id}", headers=headers).status_code == 200
    assert client.delete(f"{url}/{note_id}", headers=headers).status_code == 204
    assert client.get(f"{url}/{note_id}", headers=headers).status_code == 404


def test_validation_and_isolation(client):
    alice = user(client, "Alice")
    team = client.post("/teams", headers={"x-user-id": alice}, json={"name": "One"}).json()["id"]
    url = f"/teams/{team}/notes"
    headers = {"x-user-id": alice}
    assert client.post(url, headers=headers, json={"title": ""}).status_code == 422
    assert client.get(url, headers=headers, params={"limit": 101}).status_code == 422
    note = client.post(url, headers=headers, json={"title": "Valid"}).json()
    assert client.patch(f"{url}/{note['id']}", headers=headers, json={"title": None}).status_code == 422
    other = client.post("/teams", headers=headers, json={"name": "Two"}).json()["id"]
    assert client.get(f"/teams/{other}/notes/{note['id']}", headers=headers).status_code == 404
