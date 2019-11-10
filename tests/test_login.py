import pytest

from app import app


@pytest.fixture(scope="module")
def test_client():
    app.config["WTF_CSRF_ENABLED"] = False
    testing_client = app.test_client()
    yield testing_client


def test_home_page(test_client):
    response = test_client.get("/")
    assert response.status_code == 302


def test_login_page(test_client):
    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Username" in response.data


def test_login(test_client):
    response = test_client.post(
        "/login",
        data=dict(username="test", password="test", two_factor="12345678901"),
        follow_redirects=True,
    )

    assert b"success on login" in response.data
