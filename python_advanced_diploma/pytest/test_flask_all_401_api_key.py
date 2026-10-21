import pytest


@pytest.mark.parametrize(
    "method, endpoint",
    [
        ("GET", "/api/tweets"),
        ("POST", "/api/tweets"),
        ("DELETE", "/api/tweets/1"),
        ("POST", "/api/tweets/1/likes"),
        ("DELETE", "/api/tweets/1/likes"),
        ("POST", "/api/users/2/follow"),
        ("DELETE", "/api/users/2/follow"),
        ("GET", "/api/users/me"),
        # GET /api/users/<id> — НЕ ТРЕБУЕТ api-key (пропускаем)
    ],
)
def test_api_key_missing(client, method, endpoint):
    response = client.open(method=method, path=endpoint)
    assert response.status_code == 401
    assert response.get_json() == {
        "result": False,
        "error_type": "missing_api_key",
        "error_message": "Не передан api-key",
    }
