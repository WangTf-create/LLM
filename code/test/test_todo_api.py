"""团队待办 API 测试 — 驱动 spec: code/spec/todo_api_spec.md"""


def _register_and_token(client, username: str, password: str = "secret1") -> str:
    client.post("/auth/register", json={"username": username, "password": password})
    login = client.post("/auth/login", json={"username": username, "password": password})
    return login.json()["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _create_team(client, token: str, name: str) -> dict:
    return client.post("/teams", json={"name": name}, headers=_auth(token)).json()


def test_create_todo_success(client):
    token = _register_and_token(client, "owner1")
    team = _create_team(client, token, "TeamAlpha")
    response = client.post(
        f"/teams/{team['id']}/todos",
        json={"title": "Write tests"},
        headers=_auth(token),
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["team_id"] == team["id"]
    assert data["title"] == "Write tests"
    assert data["done"] is False
    assert data["created_by"] == 1
    assert data["created_by_username"] == "owner1"
    assert data["completed_by"] is None
    assert data["completed_by_username"] is None


def test_create_todo_empty_title_422(client):
    token = _register_and_token(client, "owner1")
    team = _create_team(client, token, "TeamAlpha")
    response = client.post(
        f"/teams/{team['id']}/todos",
        json={"title": ""},
        headers=_auth(token),
    )
    assert response.status_code == 422


def test_create_todo_blank_title_422(client):
    token = _register_and_token(client, "owner1")
    team = _create_team(client, token, "TeamAlpha")
    response = client.post(
        f"/teams/{team['id']}/todos",
        json={"title": "   "},
        headers=_auth(token),
    )
    assert response.status_code == 422


def test_create_todo_title_too_long_422(client):
    token = _register_and_token(client, "owner1")
    team = _create_team(client, token, "TeamAlpha")
    response = client.post(
        f"/teams/{team['id']}/todos",
        json={"title": "a" * 101},
        headers=_auth(token),
    )
    assert response.status_code == 422


def test_create_todo_non_member_403(client):
    owner_token = _register_and_token(client, "owner1")
    outsider_token = _register_and_token(client, "outsider")
    team = _create_team(client, owner_token, "PrivateTeam")
    response = client.post(
        f"/teams/{team['id']}/todos",
        json={"title": "Blocked"},
        headers=_auth(outsider_token),
    )
    assert response.status_code == 403


def test_create_todo_team_not_found_404(client):
    token = _register_and_token(client, "owner1")
    response = client.post(
        "/teams/999/todos",
        json={"title": "Ghost"},
        headers=_auth(token),
    )
    assert response.status_code == 404


def test_list_todos_success(client):
    token = _register_and_token(client, "owner1")
    team = _create_team(client, token, "TeamAlpha")
    client.post(
        f"/teams/{team['id']}/todos",
        json={"title": "Second"},
        headers=_auth(token),
    )
    client.post(
        f"/teams/{team['id']}/todos",
        json={"title": "First"},
        headers=_auth(token),
    )
    response = client.get(f"/teams/{team['id']}/todos", headers=_auth(token))
    assert response.status_code == 200
    titles = [item["title"] for item in response.json()]
    assert titles == ["Second", "First"]


def test_list_todos_non_member_403(client):
    owner_token = _register_and_token(client, "owner1")
    outsider_token = _register_and_token(client, "outsider")
    team = _create_team(client, owner_token, "PrivateTeam")
    response = client.get(f"/teams/{team['id']}/todos", headers=_auth(outsider_token))
    assert response.status_code == 403


def test_patch_todo_success(client):
    token = _register_and_token(client, "owner1")
    team = _create_team(client, token, "TeamAlpha")
    todo = client.post(
        f"/teams/{team['id']}/todos",
        json={"title": "Old title"},
        headers=_auth(token),
    ).json()
    response = client.patch(
        f"/teams/{team['id']}/todos/{todo['id']}",
        json={"title": "New title"},
        headers=_auth(token),
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New title"


def test_patch_todo_not_found_404(client):
    token = _register_and_token(client, "owner1")
    team = _create_team(client, token, "TeamAlpha")
    response = client.patch(
        f"/teams/{team['id']}/todos/999",
        json={"title": "New title"},
        headers=_auth(token),
    )
    assert response.status_code == 404


def test_delete_todo_success(client):
    token = _register_and_token(client, "owner1")
    team = _create_team(client, token, "TeamAlpha")
    todo = client.post(
        f"/teams/{team['id']}/todos",
        json={"title": "Remove me"},
        headers=_auth(token),
    ).json()
    response = client.delete(
        f"/teams/{team['id']}/todos/{todo['id']}",
        headers=_auth(token),
    )
    assert response.status_code == 204
    assert response.content == b""


def test_delete_todo_not_found_404(client):
    token = _register_and_token(client, "owner1")
    team = _create_team(client, token, "TeamAlpha")
    response = client.delete(
        f"/teams/{team['id']}/todos/999",
        headers=_auth(token),
    )
    assert response.status_code == 404


def test_mark_done_success(client):
    token = _register_and_token(client, "owner1")
    team = _create_team(client, token, "TeamAlpha")
    todo = client.post(
        f"/teams/{team['id']}/todos",
        json={"title": "Finish me"},
        headers=_auth(token),
    ).json()
    response = client.post(
        f"/teams/{team['id']}/todos/{todo['id']}/done",
        headers=_auth(token),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["done"] is True
    assert data["completed_by"] == 1
    assert data["completed_by_username"] == "owner1"


def test_mark_done_idempotent(client):
    owner_token = _register_and_token(client, "owner1")
    member_token = _register_and_token(client, "member1")
    team = _create_team(client, owner_token, "TeamAlpha")
    client.post(
        f"/teams/{team['id']}/members",
        json={"username": "member1"},
        headers=_auth(owner_token),
    )
    todo = client.post(
        f"/teams/{team['id']}/todos",
        json={"title": "Already done"},
        headers=_auth(owner_token),
    ).json()
    first = client.post(
        f"/teams/{team['id']}/todos/{todo['id']}/done",
        headers=_auth(owner_token),
    ).json()
    response = client.post(
        f"/teams/{team['id']}/todos/{todo['id']}/done",
        headers=_auth(member_token),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["done"] is True
    assert data["completed_by"] == first["completed_by"]
    assert data["completed_by_username"] == "owner1"


def test_mark_done_not_found_404(client):
    token = _register_and_token(client, "owner1")
    team = _create_team(client, token, "TeamAlpha")
    response = client.post(
        f"/teams/{team['id']}/todos/999/done",
        headers=_auth(token),
    )
    assert response.status_code == 404


def test_delete_then_absent_from_list_and_patch_404(client):
    token = _register_and_token(client, "owner1")
    team = _create_team(client, token, "TeamAlpha")
    todo = client.post(
        f"/teams/{team['id']}/todos",
        json={"title": "Temporary"},
        headers=_auth(token),
    ).json()
    client.delete(
        f"/teams/{team['id']}/todos/{todo['id']}",
        headers=_auth(token),
    )
    listed = client.get(f"/teams/{team['id']}/todos", headers=_auth(token)).json()
    assert all(item["id"] != todo["id"] for item in listed)
    patch = client.patch(
        f"/teams/{team['id']}/todos/{todo['id']}",
        json={"title": "Nope"},
        headers=_auth(token),
    )
    assert patch.status_code == 404
