from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app=app)


def test_serve_index_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "Skill" in response.text
    assert "Branch" in response.text


def test_serve_login_page():
    response = client.get("/pages/login.html")
    assert response.status_code == 200
    assert "Log in to SkillBranch" in response.text


def test_serve_static_config_js():
    response = client.get("/js/shared/config.js")
    assert response.status_code == 200
    assert 'export const API_BASE_URL = ""' in response.text
