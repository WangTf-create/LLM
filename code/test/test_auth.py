"""认证 API 测试 — 驱动 spec: code/spec/auth_spec.md"""


def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={"username": "alice", "password": "secret1"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "alice"
    assert "password" not in data
    assert "password_hash" not in data


def test_register_empty_username_422(client):
    response = client.post(
        "/auth/register",
        json={"username": "", "password": "secret1"},
    )
    assert response.status_code == 422


def test_register_short_username_422(client):
    response = client.post(
        "/auth/register",
        json={"username": "ab", "password": "secret1"},
    )
    assert response.status_code == 422


def test_register_invalid_username_422(client):
    response = client.post(
        "/auth/register",
        json={"username": "user-name", "password": "secret1"},
    )
    assert response.status_code == 422


def test_register_short_password_422(client):
    response = client.post(
        "/auth/register",
        json={"username": "alice", "password": "12345"},
    )
    assert response.status_code == 422


def test_register_duplicate_username_409(client):
    client.post("/auth/register", json={"username": "alice", "password": "secret1"})
    response = client.post(
        "/auth/register",
        json={"username": "alice", "password": "other12"},
    )
    assert response.status_code == 409


def test_login_success(client):
    client.post("/auth/register", json={"username": "alice", "password": "secret1"})
    response = client.post(
        "/auth/login",
        json={"username": "alice", "password": "secret1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


def test_login_wrong_password_401(client):
    client.post("/auth/register", json={"username": "alice", "password": "secret1"})
    response = client.post(
        "/auth/login",
        json={"username": "alice", "password": "wrongpass"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user_401(client):
    response = client.post(
        "/auth/login",
        json={"username": "nobody", "password": "secret1"},
    )
    assert response.status_code == 401


def test_me_success(client):
    client.post("/auth/register", json={"username": "alice", "password": "secret1"})
    login = client.post(
        "/auth/login",
        json={"username": "alice", "password": "secret1"},
    )
    token = login.json()["access_token"]
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
    assert "password" not in data


def test_me_no_authorization_401(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_invalid_token_401(client):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid.token.here"},
    )
    assert response.status_code == 401
