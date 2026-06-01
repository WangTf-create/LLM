"""前端冒烟测试 — 驱动 spec: code/spec/todo_ui_spec.md"""

from fastapi.testclient import TestClient

from app import app


def test_static_index_page():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "Team Todo" in response.text
    assert 'src="/app.js"' in response.text
    assert 'href="/style.css"' in response.text


def test_static_assets():
    client = TestClient(app)
    for path in ("/app.js", "/style.css"):
        response = client.get(path)
        assert response.status_code == 200
        assert len(response.content) > 0


def test_app_js_openapi_constraints():
    client = TestClient(app)
    js = client.get("/app.js").text
    assert 'TOKEN_KEY = "access_token"' in js
    assert "Authorization" in js
    assert 'maxlength="100"' in js
    assert 'maxlength="50"' in js
    assert "协作记录" in js
    assert "创建者" in js
    assert "完成者" in js


def test_app_js_routes_and_flows():
    client = TestClient(app)
    js = client.get("/app.js").text
    assert "#/login" in js or '"/login"' in js
    assert "#/register" in js or '"/register"' in js
    assert "#/teams" in js or '"/teams"' in js
    assert "/auth/register" in js
    assert "/auth/login" in js
    assert "/teams/" in js
    assert "/todos" in js
    assert "confirm(" in js


def test_openapi_json_available():
    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "Team Todo API"
    assert "/auth/login" in schema["paths"]
    assert "TodoPublic" in schema["components"]["schemas"]
