import pytest

from pytest_mock import mocker

from app import app


@pytest.fixture(scope="module")
def test_client():
    app.config["WTF_CSRF_ENABLED"] = False
    testing_client = app.test_client()
    yield testing_client


def test_login_activity(test_client):
    login_response = test_client.post(
        "/login",
        data=dict(username="admin", password="Administrator@1",),
        follow_redirects=True,
    )
    assert login_response.status_code == 200

    user_activity_response = test_client.post(
        "/login_history", data=dict(username="admin",), follow_redirects=True
    )

    assert user_activity_response.status_code == 200
    assert b'id="login' in user_activity_response.data
    assert b"login time:" in user_activity_response.data


def test_logout_activity(test_client):
    login_response = test_client.post(
        "/login",
        data=dict(username="admin", password="Administrator@1",),
        follow_redirects=True,
    )
    assert login_response.status_code == 200

    logout_response = test_client.get("/logout")
    logout_response.status_code == 302

    login_response = test_client.post(
        "/login",
        data=dict(username="admin", password="Administrator@1",),
        follow_redirects=True,
    )

    assert login_response.status_code == 200

    user_activity_response = test_client.post(
        "/login_history", data=dict(username="admin",), follow_redirects=True
    )

    assert b'id="logout' in user_activity_response.data
