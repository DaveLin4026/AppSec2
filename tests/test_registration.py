import pytest

from app import app


@pytest.fixture(scope="module")
def test_client():
    flask_app = app
    testing_client = flask_app.test_client()
    yield testing_client


def test_registration_page(test_client):
    response = test_client.get("/register")
    assert response.status_code == 200
    assert b"Register" in response.data
    assert b"Username" in response.data
    assert b"2fa" in response.data


def test_registration(test_client):
    response = test_client.post(
        "/register",
        data=dict(username="unit_test_registration_user", password="test",),
        follow_redirects=True,
    )
    assert b"registration success" in response.data
