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


@pytest.mark.tweets
class TestTweets:

    def test_get_api_tweets_good_200(self, client):
        headers = {"api-key": "api_key1"}
        tweets = client.get("/api/tweets", headers=headers)
        assert tweets.status_code == 200
        assert tweets.get_json() == {'result': True, 'tweets': [
            {'id': 1, 'content': 'This is the content user1', 'attachments': [], 'author': {'id': 1, 'name': 'user1'},
             'likes': []},
            {'id': 2, 'content': 'This is the content user2', 'attachments': [], 'author': {'id': 2, 'name': 'user2'},
             'likes': []}]}

    def test_get_api_tweets_bad_404(self, client):
        headers = {"api-key": "api_key"}
        tweets = client.get("/api/tweets", headers=headers)
        assert tweets.status_code == 404
        assert tweets.get_json() == {
            "result": False,
            "error_type": "user_not_found",
            "error_message": "Пользователь не найден",
        }

    def test_get_create_tweets_good_201(self, client):
        headers = {"api-key": "api_key1"}
        body = {"tweet_data": "new tweet test api_key1(user_1)"}
        tweets = client.post("/api/tweets", headers=headers, json=body)
        assert tweets.status_code == 201
        assert tweets.get_json() == {"result": True, "tweet_id": 3}

    def test_get_create_tweets_bad_404(self, client):
        headers = {"api-key": "api_key"}
        body = {"tweet_data": "new tweet test api_key1(user_1)"}
        tweets = client.post("/api/tweets", headers=headers, json=body)
        assert tweets.status_code == 404
        assert tweets.get_json() == {
            "result": False,
            "error_type": "user_not_found",
            "error_message": "Пользователь не найден",
        }

    def test_get_create_tweets_bad_400(self, client):
        headers = {"api-key": "api_key1"}
        body = {"tweet_data": ""}
        tweets = client.post("/api/tweets", headers=headers, json=body)
        assert tweets.status_code == 400
        assert tweets.get_json() == {
            "message": {"tweet_data": ["Длина поста больше 1 буквы"]}
        }

    def test_delete_api_tweets_id_good(self, client):
        headers = {"api-key": "api_key1"}
        body = {"tweet_data": "deleted tweet id"}
        tweets = client.post("/api/tweets", headers=headers, json=body)
        tweet_id = tweets.get_json()["tweet_id"]
        deleted_tweet = client.delete(
            "/api/tweets/{}".format(tweet_id), headers=headers
        )
        assert deleted_tweet.status_code == 200
        assert deleted_tweet.get_json() == {"result": True}

    def test_delete_api_tweets_id_bad_404(self, client):
        headers = {"api-key": "api_key"}
        deleted_tweet = client.delete("/api/tweets/{}".format(3), headers=headers)
        assert deleted_tweet.status_code == 404
        assert deleted_tweet.get_json() == {
            "result": False,
            "error_type": "user_not_found",
            "error_message": "Пользователь не найден",
        }

    def test_delete_api_tweets_id_bad_403(self, client):
        headers = {"api-key": "api_key2"}
        body = {"tweet_data": "new tweet test api_key1(user_1)"}
        tweets = client.post("/api/tweets", headers=headers, json=body)
        tweets_id = tweets.get_json()["tweet_id"]
        headers = {"api-key": "api_key1"}
        deleted_tweet = client.delete(
            "/api/tweets/{}".format(tweets_id), headers=headers
        )
        assert deleted_tweet.status_code == 403
        assert deleted_tweet.get_json() == {
            "result": False,
            "error_type": "author_not_found",
            "error_message": "У вас нет прав",
        }


@pytest.mark.tweets_like
class TestTweets_like:
    def test_get_likes_good_201(self, client):
        headers = {"api-key": "api_key2"}
        body = {"tweet_data": "new tweet test api_key1(user_1)"}
        tweets = client.post("/api/tweets", headers=headers, json=body)
        tweets_id = tweets.get_json()["tweet_id"]
        headers = {"api-key": "api_key1"}
        tweets_like = client.post(
            "/api/tweets/{}/likes".format(tweets_id), headers=headers
        )
        assert tweets_like.status_code == 201
        assert tweets_like.get_json() == {"result": True}

    def test_get_likes_bad_user_404(self, client):
        headers = {"api-key": "api_key"}
        tweets_like = client.post("/api/tweets/{}/likes".format(3), headers=headers)
        assert tweets_like.status_code == 404
        assert tweets_like.get_json() == {
            "result": False,
            "error_type": "user_not_found",
            "error_message": "Пользователь не найден",
        }

    def test_get_likes_bad_tweet_404(self, client):
        headers = {"api-key": "api_key1"}
        tweets_like = client.post("/api/tweets/{}/likes".format(3), headers=headers)
        assert tweets_like.status_code == 404
        assert tweets_like.get_json() == {
            "result": False,
            "error_type": "tweet_not_found",
            "error_message": "Пост не найден",
        }

    def test_get_likes_bad_409(self, client):
        headers = {"api-key": "api_key2"}
        body = {"tweet_data": "new tweet test api_key1(user_1)"}
        tweets = client.post("/api/tweets", headers=headers, json=body)
        tweets_id = tweets.get_json()["tweet_id"]
        headers = {"api-key": "api_key1"}
        client.post("/api/tweets/{}/likes".format(tweets_id), headers=headers)
        tweets_like_2 = client.post(
            "/api/tweets/{}/likes".format(tweets_id), headers=headers
        )
        assert tweets_like_2.status_code == 409
        assert tweets_like_2.get_json() == {
            "result": False,
            "error_type": "like is found",
            "error_message": "Вы уже ставили под этим постом лайк",
        }

    def test_delete_likes_good_200(self, client):
        headers = {"api-key": "api_key2"}
        body = {"tweet_data": "new tweet test api_key1(user_1)"}
        tweets = client.post("/api/tweets", headers=headers, json=body)
        tweets_id = tweets.get_json()["tweet_id"]
        headers = {"api-key": "api_key1"}
        client.post("/api/tweets/{}/likes".format(tweets_id), headers=headers)
        tweets_delete = client.delete(
            "/api/tweets/{}/likes".format(tweets_id), headers=headers
        )
        assert tweets_delete.status_code == 200
        assert tweets_delete.get_json() == {"result": True}

    def test_delete_likes_bad_user_404(self, client):
        headers = {"api-key": "api_key"}
        tweets_like = client.delete("/api/tweets/{}/likes".format(3), headers=headers)
        assert tweets_like.status_code == 404
        assert tweets_like.get_json() == {
            "result": False,
            "error_type": "user_not_found",
            "error_message": "Пользователь не найден",
        }

    def test_delete_likes_bad_tweet_404(self, client):
        headers = {"api-key": "api_key1"}
        tweets_like = client.delete("/api/tweets/{}/likes".format(3), headers=headers)
        assert tweets_like.status_code == 404
        assert tweets_like.get_json() == {
            "result": False,
            "error_type": "tweet_not_found",
            "error_message": "Пост не найден",
        }

    def test_delete_likes_bad_409(self, client):
        headers = {"api-key": "api_key2"}
        body = {"tweet_data": "new tweet test api_key1(user_1)"}
        tweets = client.post("/api/tweets", headers=headers, json=body)
        tweets_id = tweets.get_json()["tweet_id"]
        headers = {"api-key": "api_key1"}
        tweets_like_2 = client.delete(
            "/api/tweets/{}/likes".format(tweets_id), headers=headers
        )
        assert tweets_like_2.status_code == 409
        assert tweets_like_2.get_json() == {
            "result": False,
            "error_type": "like is not found",
            "error_message": "Вы не ставили лайк под этим постом",
        }


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
