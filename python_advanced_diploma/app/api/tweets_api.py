import logging.config

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app.extensions import dict_config_api
from app.models.crud.tweet_crud import (
    AuthorTweetError,
    LikeTweetError,
    MediaAlreadyAttachedError,
    MediaNotFoundError,
    TweetNotFoundError,
    UserNotFoundErrorTweet,
    crud_create_tweet,
    crud_created_like_tweet,
    crud_delete_like_tweet,
    crud_delete_tweet_id,
)
from app.models.crud.user_crud import UserNotFoundError, crud_user_tweets
from app.schemas.tweets_schemas import TweetSchema

logging.config.dictConfig(dict_config_api)
logger = logging.getLogger("api_logger")


class Tweets(Resource):
    def get(self):
        """
        Получить ленту твитов пользователей на которых ты подписан
        ---
        tags:
          - Tweets
        parameters:
          - name: api-key
            in: header
            type: string
            required: true
            description: API-ключ пользователя
        responses:
          200:
            description: Успешный ответ
            schema:
              type: object
              properties:
                result:
                  type: boolean
                  example: true
                tweets:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        example: 8
                      content:
                        type: string
                        example: "Твит от user_3: Сегодня отличная погода!"
                      attachments:
                        type: array
                        items:
                          type: string
                        example: []
                      author:
                        type: object
                        properties:
                          id:
                            type: integer
                            example: 2
                          name:
                            type: string
                            example: "user_3"
                      likes:
                        type: array
                        items:
                          type: object
                          properties:
                            user_id:
                              type: integer
                              example: 2
                            name:
                              type: string
                              example: "user_3"
                        example: []
          401:
            description: Не передан api-key
            schema:
              type: object
              properties:
                result:
                  type: boolean
                  example: false
                error_type:
                  type: string
                  example: "missing_api_key"
                error_message:
                  type: string
                  example: "Не передан api-key"
          404:
            description: Пользователь не найден
            schema:
              type: object
              properties:
                result:
                  type: boolean
                  example: false
                error_type:
                  type: string
                  example: "user_not_found"
                error_message:
                  type: string
                  example: "Пользователь не найден"
          500:
            description: Внутренняя ошибка сервера
            schema:
              type: object
              properties:
                result:
                  type: boolean
                  example: false
                error_type:
                  type: string
                  example: "internal_server_error"
                error_message:
                  type: string
                  example: "Внутренняя ошибка сервера"
        """
        logger.debug("start Tweets.get")
        api_key = request.headers.get("api-key")
        if not api_key or api_key.strip() == "":
            logger.warning("Tweets.post: no api-key provided")
            return {
                "result": False,
                "error_type": "missing_api_key",
                "error_message": "Не передан api-key",
            }, 401
        try:
            logger.debug("start crud tweets")
            tweet_data = crud_user_tweets(api_key=api_key)
            tweets_data = []

            for tweet in tweet_data:
                result = {}
                result["id"] = tweet.id
                result["content"] = tweet.content
                result["attachments"] = (
                    [media.file_path for media in tweet.media] if tweet.media else []
                )
                result["author"] = {
                    "id": tweet.author_id,
                    "name": tweet.user.name,
                }
                result["likes"] = (
                    [
                        {"user_id": like.user.id, "name": like.user.name}
                        for like in tweet.likes
                    ]
                    if tweet.likes
                    else []
                )
                tweets_data.append(result)
            logger.debug("finish crud tweets")
            return {"result": True, "tweets": tweets_data}
        except UserNotFoundError:
            logger.warning("Tweets.ger: user not found error")
            return {
                "result": False,
                "error_type": "user_not_found",
                "error_message": "Пользователь не найден",
            }, 404
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "result": False,
                "error_type": "internal_server_error",
                "error_message": "Внутренняя ошибка сервера",
            }, 500

    def post(self):
        """
        Создать пост
        ---
        tags:
          - Tweets
        parameters:
          - name: api-key
            in: header
            type: string
            required: true
            description: API-ключ пользователя
          - name: body
            in: body
            required: true
            description: Данные для создания твита
            schema:
              type: object
              properties:
                tweet_data:
                  type: string
                  example: "Мой новый твит"
                tweet_media_ids:
                  type: array
                  items:
                    type: integer
                  example: [1, 2, 3]
        responses:
          200:
            description: Успешный ответ
            schema:
              type: object
              properties:
                result:
                  type: boolean
                  example: true
                tweet_id:
                  type: integer
                  example: 2
          400:
            description: Ошибка валидации
            schema:
              type: object
              properties:
                result:
                  type: boolean
                  example: false
                error_type:
                  type: string
                  example: "validation_error"
                error_message:
                  type: string
                  example: "tweet_data обязательное поле"
          401:
            description: Не передан api-key
            schema:
              type: object
              properties:
                result:
                  type: boolean
                  example: false
                error_type:
                  type: string
                  example: "missing_api_key"
                error_message:
                  type: string
                  example: "Не передан api-key"
          404:
            description: Пользователь или медиа не найдены
            schema:
              type: object
              properties:
                result:
                  type: boolean
                  example: false
                error_type:
                  type: string
                  example: "user_not_found"
                error_message:
                  type: string
                  example: "Пользователь не найден"
          500:
            description: Внутренняя ошибка сервера
            schema:
              type: object
              properties:
                result:
                  type: boolean
                  example: false
                error_type:
                  type: string
                  example: "internal_server_error"
                error_message:
                  type: string
                  example: "Внутренняя ошибка сервера"
        """
        logger.debug("start Tweets.post")
        api_key = request.headers.get("api-key")
        if not api_key:
            logger.warning("Tweets.post: no api-key provided")
            return {
                "result": False,
                "error_type": "missing_api_key",
                "error_message": "Не передан api-key",
            }, 401
        schema_tweet = TweetSchema()
        logger.debug("start TweetSchema")
        try:
            tweet_data = schema_tweet.load(request.json)
            logger.debug("start ValidatorTweetSchema")
        except ValidationError as err:
            logger.warning(f"ValidatorTweetSchema is error {err.messages}")
            return {"message": err.messages}, 400
        try:
            tweet_content = tweet_data["tweet_data"]
            tweet_media = tweet_data.get("tweet_media_ids", None)
            logger.debug("start crud_create_tweet")
            tweet = crud_create_tweet(
                api_key=api_key, content=tweet_content, media_ids=tweet_media
            )
            logger.debug("finish TweetPost")
            return {"result": True, "tweet_id": tweet.id}, 201
        except UserNotFoundErrorTweet:
            logger.warning("Tweets.post: user not found error")
            return {
                "result": False,
                "error_type": "user_not_found",
                "error_message": "Пользователь не найден",
            }, 404
        except MediaAlreadyAttachedError:
            logger.warning("Tweets.post: media already attached error")
            return {
                "result": False,
                "error_type": "media_already_attached",
                "error_message": "Медиафайл уже привязан к другому твиту",
            }, 409
        except MediaNotFoundError:
            logger.warning("Tweets.post: media not found error")
            return {
                "result": False,
                "error_type": "media_not_found",
                "error_message": "Медиафайл не найден",
            }, 404
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "result": False,
                "error_type": "internal_server_error",
                "error_message": "Внутренняя ошибка сервера",
            }, 500


class TweetDelete(Resource):
    def delete(self, tweet_id):
        """
        Удалить пост
        ---
        tags:
          - Tweets
        parameters:
          - name: api-key
            in: header
            required: true
            type: string
            description: API-ключ пользователя
          - name: tweet_id
            in: path
            required: true
            type: integer
            example: 1
            description: ID твита для удаления
        responses:
          200:
            description: Успешный ответ
            schema:
              type: object
              properties:
                result:
                  type: boolean
                  example: true
          401:
            description: Не передан api-key
            schema:
              type: object
              properties:
                result:
                  type: boolean
                  example: false
                error_type:
                  type: string
                  example: "missing_api_key"
                error_message:
                  type: string
                  example: "Не передан api-key"
          404:
            description: |
              Объект не найден. Возможные варианты:
              - Пользователь не найден (error_type: user_not_found)
              - Твит не найден (error_type: tweet_not_found)
            schema:
              type: object
              properties:
                result:
                  type: boolean
                  example: false
                error_type:
                  type: string
                  example: "user_not_found"
                error_message:
                  type: string
                  example: "Пользователь не найден"
          403:
            description: Ошибка прав доступа
            schema:
              type: object
              properties:
                result:
                  type: boolean
                  example: false
                error_type:
                  type: string
                  example: "author_not_found"
                error_message:
                  type: string
                  example: "У вас нет прав"
          500:
            description: Внутренняя ошибка сервера
            schema:
              type: object
              properties:
                result:
                  type: boolean
                  example: false
                error_type:
                  type: string
                  example: "internal_server_error"
                error_message:
                  type: string
                  example: "Внутренняя ошибка сервера"
        """
        logger.debug("start Tweets.delete")
        api_key = request.headers.get("api-key")
        if not api_key:
            logger.warning("Tweets.post: no api-key provided")
            return {
                "result": False,
                "error_type": "missing_api_key",
                "error_message": "Не передан api-key",
            }, 401
        try:
            logger.debug("start Tweets.delete")
            crud_delete_tweet_id(api_key=api_key, tweet_id=tweet_id)
            logger.debug("finish TweetDelete")
            return {"result": True}
        except UserNotFoundErrorTweet:
            logger.warning("Tweets.post: user not found error")
            return {
                "result": False,
                "error_type": "user_not_found",
                "error_message": "Пользователь не найден",
            }, 404
        except TweetNotFoundError:
            logger.warning("Tweets.post: tweet not found error")
            return {
                "result": False,
                "error_type": "tweet_not_found",
                "error_message": "Пост не найден",
            }, 404
        except AuthorTweetError:
            logger.warning("Tweets.post: author not found error")
            return {
                "result": False,
                "error_type": "author_not_found",
                "error_message": "У вас нет прав",
            }, 403
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "result": False,
                "error_type": "internal_server_error",
                "error_message": "Внутренняя ошибка сервера",
            }, 500


class TweetLike(Resource):
    def post(self, tweet_id):
        """
        Поставить лайк под пост
        ---
        tags:
            - Tweets Like
        parameters:
            - name: api-key
              in: header
              required: true
              type: string
              description: API-ключ пользователя
            - name: tweet_id
              in: path
              required: true
              type: string
        responses:
            200:
                description: Успешный ответ
                schema:
                    properties:
                        result:
                            type: boolean
                            example: true
            401:
                description: Не передан api-key
                schema:
                  type: object
                  properties:
                    result:
                      type: boolean
                      example: false
                    error_type:
                      type: string
                      example: "missing_api_key"
                    error_message:
                      type: string
                      example: "Не передан api-key"
            404:
                description: |
                  Объект не найден. Возможные варианты:
                  - Пользователь не найден (error_type: user_not_found)
                  - Твит не найден (error_type: tweet_not_found)
                schema:
                  type: object
                  properties:
                    result:
                      type: boolean
                      example: false
                    error_type:
                      type: string
                      example: "user_not_found"
                    error_message:
                      type: string
                      example: "Пользователь не найден"
            409:
                description: Вы уже ставили под этим постом лайк
                schema:
                    type: object
                    properties:
                        result:
                            type: boolean
                            example: false
                        error_type:
                            type: string
                            example: internal_server_error
                        error_message:
                            type: string
                            example: Вы уже ставили под этим постом лайк
            500:
                description: Внутренняя ошибка сервера
                schema:
                  type: object
                  properties:
                    result:
                      type: boolean
                      example: false
                    error_type:
                      type: string
                      example: "internal_server_error"
                    error_message:
                      type: string
                      example: "Внутренняя ошибка сервера"
        """
        logger.debug("start TweetLike.post")
        api_key = request.headers.get("api-key")
        if not api_key:
            logger.warning("Tweets.post: no api-key provided")
            return {
                "result": False,
                "error_type": "missing_api_key",
                "error_message": "Не передан api-key",
            }, 401
        try:
            logger.debug("start TweetLike.post")
            crud_created_like_tweet(api_key=api_key, tweet_id=tweet_id)
            logger.debug("finish TweetLike")
            return {"result": True}, 201
        except UserNotFoundErrorTweet:
            logger.warning("Tweets.post: user not found error")
            return {
                "result": False,
                "error_type": "user_not_found",
                "error_message": "Пользователь не найден",
            }, 404
        except TweetNotFoundError:
            logger.warning("Tweets.post: tweet not found error")
            return {
                "result": False,
                "error_type": "tweet_not_found",
                "error_message": "Пост не найден",
            }, 404
        except LikeTweetError:
            logger.warning("Tweets.post: author not found error")
            return {
                "result": False,
                "error_type": "like is found",
                "error_message": "Вы уже ставили под этим постом лайк",
            }, 409
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "result": False,
                "error_type": "internal_server_error",
                "error_message": "Внутренняя ошибка сервера",
            }, 500

    def delete(self, tweet_id):
        """
        Убрать лайк
        ---
        tags:
            - Tweets Like
        parameters:
            - name: api-key
              in: header
              required: true
              type: string
              description: API-ключ пользователя
            - name: tweet_id
              in: path
              required: true
              type: string
              example: 1
              description: ID твита для удаления
        responses:
            200:
                description: Успешный ответ
                schema:
                    properties:
                        result:
                            type: boolean
                            example: true
            401:
                description: Не передан api-key
                schema:
                  type: object
                  properties:
                    result:
                        type: boolean
                        example: false
                    error_type:
                        type: string
                        example: "missing_api_key"
                    error_message:
                        type: string
                        example: "Не передан api-key"
            404:
                description: |
                      Объект не найден. Возможные варианты:
                      - Пользователь не найден (error_type: user_not_found)
                      - Твит не найден (error_type: tweet_not_found)
                schema:
                    type: object
                    properties:
                        result:
                          type: boolean
                          example: false
                        error_type:
                          type: string
                          example: "user_not_found"
                        error_message:
                          type: string
                          example: "Пользователь не найден"
            409:
                description: Вы уже ставили под этим постом лайк
                schema:
                        type: object
                        properties:
                            result:
                                type: boolean
                                example: false
                            error_type:
                                type: string
                                example: internal_server_error
                            error_message:
                                type: string
                                example: Вы не ставили под этим постом лайк
            500:
                description: Внутренняя ошибка сервера
                schema:
                      type: object
                      properties:
                        result:
                          type: boolean
                          example: false
                        error_type:
                          type: string
                          example: "internal_server_error"
                        error_message:
                          type: string
                          example: "Внутренняя ошибка сервера"
        """
        logger.debug("start TweetLike.delete")
        api_key = request.headers.get("api-key")
        if not api_key:
            logger.warning("Tweets.delete: no api-key provided")
            return {
                "result": False,
                "error_type": "missing_api_key",
                "error_message": "Не передан api-key",
            }, 401
        try:
            logger.debug("start TweetLike.delete")
            crud_delete_like_tweet(api_key=api_key, tweet_id=tweet_id)
            logger.debug("finish TweetLike")
            return {"result": True}
        except UserNotFoundErrorTweet:
            logger.warning("Tweets.post: user not found error")
            return {
                "result": False,
                "error_type": "user_not_found",
                "error_message": "Пользователь не найден",
            }, 404
        except TweetNotFoundError:
            logger.warning("Tweets.post: tweet not found error")
            return {
                "result": False,
                "error_type": "tweet_not_found",
                "error_message": "Пост не найден",
            }, 404
        except LikeTweetError:
            logger.warning("Tweets.post: author not found error")
            return {
                "result": False,
                "error_type": "like is not found",
                "error_message": "Вы не ставили лайк под этим постом",
            }, 409
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "result": False,
                "error_type": "internal_server_error",
                "error_message": "Внутренняя ошибка сервера",
            }
