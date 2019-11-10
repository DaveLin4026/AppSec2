import pytest

from pytest_mock import mocker

from app import app


@pytest.fixture(scope="module")
def test_client():
    app.config["WTF_CSRF_ENABLED"] = False
    testing_client = app.test_client()
    yield testing_client


def test_history(test_client, mocker):
    login_response = test_client.post(
        "/login", data=dict(username="test", password="test",), follow_redirects=True,
    )
    assert login_response.status_code == 200

    mock_check = mocker.patch("app.run_spell_check")
    mock_check.return_value = "stuff"
    spell_check_response = test_client.post(
        "/spell_check", data=dict(inputarea="test data"), follow_redirects=True,
    )
    assert spell_check_response.status_code == 200
    assert b"test data" in spell_check_response.data

    history_response = test_client.get("/history")
    assert history_response.status_code == 200
    assert b'<p id="numqueries">1</p>' in history_response.data
    assert (
        b'<li><a href="/history/query1" id="query1">Query #1</a></li>'
        in history_response.data
    )
