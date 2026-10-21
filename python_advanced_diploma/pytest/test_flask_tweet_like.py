import pytest


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
