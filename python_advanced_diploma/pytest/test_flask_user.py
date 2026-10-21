import pytest


@pytest.mark.users
class TestUser:

    def test_get_likes_good_200(self, client):
        headers = {"api-key": "api_key1"}
        response = client.get("/api/users/me", headers=headers)
        assert response.status_code == 200
        assert response.get_json() == {
            "result": True,
            "user": {
                "followers": [],
                "following": [{"id": 2, "name": "user2"}],
                "id": 1,
                "name": "user1",
            },
        }

    def test_get_likes_bad_user_404(self, client):
        headers = {"api-key": "api_key"}
        response = client.get("/api/users/me", headers=headers)
        assert response.status_code == 404
        assert response.get_json() == {
            "result": False,
            "error_type": "user_not_found",
            "error_message": "Пользователь не надйен",
        }

    def test_get_user_id_good_200(self, client):
        response = client.get("/api/users/{}".format(1))
        assert response.status_code == 200
        assert response.get_json() == {
            "result": True,
            "user": {
                "followers": [],
                "following": [{"id": 2, "name": "user2"}],
                "id": 1,
                "name": "user1",
            },
        }

    def test_get_user_id_bad_user_404(self, client):
        response = client.get("/api/users/{}".format(999))
        assert response.status_code == 404
        assert response.get_json() == {
            "result": False,
            "error_type": "user_not_found",
            "error_message": "Пользователь не надйен",
        }

    def test_post_followers_good_201(self, client):
        headers = {"api-key": "api_key1"}
        user_id = 3
        response = client.post("/api/users/{}/follow".format(user_id), headers=headers)
        assert response.status_code == 201
        assert response.get_json() == {"result": True}

    def test_post_followers_bad_user_404(self, client):
        headers = {"api-key": "api_key1"}
        response = client.post("/api/users/{}/follow".format(999), headers=headers)
        assert response.status_code == 404
        assert response.get_json() == {
            "result": False,
            "error_type": "user_not_found",
            "error_message": "Пользователь не найден",
        }

    def test_post_followers_bad_tweet_409(self, client):
        headers = {"api-key": "api_key1"}
        user_id = 3
        client.post("/api/users/{}/follow".format(user_id), headers=headers)
        response = client.post("/api/users/{}/follow".format(user_id), headers=headers)
        assert response.status_code == 409
        assert response.get_json() == {
            "result": False,
            "error_type": "user in follower",
            "error_message": "Вы уже подписаны на данного user",
        }

    def test_delete_followers_good_200(self, client):
        headers = {"api-key": "api_key1"}
        user_id = 2
        response = client.delete(
            "/api/users/{}/follow".format(user_id), headers=headers
        )
        assert response.status_code == 200
        assert response.get_json() == {"result": True}

    def test_delete_followers_bad_user_404(self, client):
        headers = {"api-key": "api_key1"}
        response = client.delete("/api/users/{}/follow".format(999), headers=headers)
        assert response.status_code == 404
        assert response.get_json() == {
            "result": False,
            "error_type": "user_not_found",
            "error_message": "Пользователь не найден",
        }

    def test_delete_followers_bad_tweet_409(self, client):
        headers = {"api-key": "api_key1"}
        user_id = 2
        client.delete("/api/users/{}/follow".format(user_id), headers=headers)
        response = client.delete(
            "/api/users/{}/follow".format(user_id), headers=headers
        )
        assert response.status_code == 409
        assert response.get_json() == {
            "result": False,
            "error_type": "user in follower",
            "error_message": "Вы не подписаны на данного user",
        }
