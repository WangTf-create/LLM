"""团队 API 测试 — 驱动 spec: code/spec/team_spec.md"""


def _register_and_token(client, username: str, password: str = "secret1") -> str:
    client.post("/auth/register", json={"username": username, "password": password})
    login = client.post("/auth/login", json={"username": username, "password": password})
    return login.json()["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_create_team_success(client):
    token = _register_and_token(client, "owner1")
    response = client.post(
        "/teams",
        json={"name": "Engineering"},
        headers=_auth(token),
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Engineering"
    assert data["created_by"] == 1
    assert data["created_by_username"] == "owner1"


def test_create_team_empty_name_422(client):
    token = _register_and_token(client, "owner1")
    response = client.post("/teams", json={"name": ""}, headers=_auth(token))
    assert response.status_code == 422


def test_create_team_blank_name_422(client):
    token = _register_and_token(client, "owner1")
    response = client.post("/teams", json={"name": "   "}, headers=_auth(token))
    assert response.status_code == 422


def test_create_team_name_too_long_422(client):
    token = _register_and_token(client, "owner1")
    response = client.post(
        "/teams",
        json={"name": "a" * 51},
        headers=_auth(token),
    )
    assert response.status_code == 422


def test_create_team_duplicate_name_409(client):
    token = _register_and_token(client, "owner1")
    client.post("/teams", json={"name": "Engineering"}, headers=_auth(token))
    response = client.post(
        "/teams",
        json={"name": "Engineering"},
        headers=_auth(token),
    )
    assert response.status_code == 409


def test_list_teams_success(client):
    token = _register_and_token(client, "owner1")
    client.post("/teams", json={"name": "Beta"}, headers=_auth(token))
    client.post("/teams", json={"name": "Alpha"}, headers=_auth(token))
    response = client.get("/teams", headers=_auth(token))
    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert names == ["Beta", "Alpha"]


def test_get_team_success(client):
    token = _register_and_token(client, "owner1")
    created = client.post(
        "/teams",
        json={"name": "Engineering"},
        headers=_auth(token),
    ).json()
    response = client.get(f"/teams/{created['id']}", headers=_auth(token))
    assert response.status_code == 200
    assert response.json()["name"] == "Engineering"


def test_get_team_non_member_403(client):
    owner_token = _register_and_token(client, "owner1")
    outsider_token = _register_and_token(client, "outsider")
    created = client.post(
        "/teams",
        json={"name": "Private"},
        headers=_auth(owner_token),
    ).json()
    response = client.get(f"/teams/{created['id']}", headers=_auth(outsider_token))
    assert response.status_code == 403


def test_get_team_not_found_404(client):
    token = _register_and_token(client, "owner1")
    response = client.get("/teams/999", headers=_auth(token))
    assert response.status_code == 404


def test_invite_member_success(client):
    owner_token = _register_and_token(client, "owner1")
    _register_and_token(client, "member1")
    team = client.post(
        "/teams",
        json={"name": "Engineering"},
        headers=_auth(owner_token),
    ).json()
    response = client.post(
        f"/teams/{team['id']}/members",
        json={"username": "member1"},
        headers=_auth(owner_token),
    )
    assert response.status_code == 201
    data = response.json()
    assert data["team_id"] == team["id"]
    assert data["user_id"] == 2
    assert data["role"] == "member"


def test_invite_member_not_owner_403(client):
    owner_token = _register_and_token(client, "owner1")
    member_token = _register_and_token(client, "member1")
    team = client.post(
        "/teams",
        json={"name": "Engineering"},
        headers=_auth(owner_token),
    ).json()
    client.post(
        f"/teams/{team['id']}/members",
        json={"username": "member1"},
        headers=_auth(owner_token),
    )
    response = client.post(
        f"/teams/{team['id']}/members",
        json={"username": "owner1"},
        headers=_auth(member_token),
    )
    assert response.status_code == 403


def test_invite_nonexistent_user_404(client):
    token = _register_and_token(client, "owner1")
    team = client.post(
        "/teams",
        json={"name": "Engineering"},
        headers=_auth(token),
    ).json()
    response = client.post(
        f"/teams/{team['id']}/members",
        json={"username": "ghost"},
        headers=_auth(token),
    )
    assert response.status_code == 404


def test_invite_duplicate_member_409(client):
    owner_token = _register_and_token(client, "owner1")
    _register_and_token(client, "member1")
    team = client.post(
        "/teams",
        json={"name": "Engineering"},
        headers=_auth(owner_token),
    ).json()
    client.post(
        f"/teams/{team['id']}/members",
        json={"username": "member1"},
        headers=_auth(owner_token),
    )
    response = client.post(
        f"/teams/{team['id']}/members",
        json={"username": "member1"},
        headers=_auth(owner_token),
    )
    assert response.status_code == 409


def test_teams_require_auth_401(client):
    response = client.get("/teams")
    assert response.status_code == 401
