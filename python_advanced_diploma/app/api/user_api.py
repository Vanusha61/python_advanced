import logging.config

from flask import jsonify, request
from flask_restful import Resource

from app.extensions import dict_config_api
from app.models.crud.user_crud import (
    FollowNotFoundError,
    UserNotFoundError,
    crud_delete_user_follow,
    crud_user_follower,
    crud_user_id,
    crud_user_me,
)

logging.config.dictConfig(dict_config_api)
logger = logging.getLogger("api_logger")


class UserMe(Resource):
    def get(self):
        """
         Информация о меом профиле
        ---
        tags:
            - UserMe
        parameters:
            - name: api-key
              in: header
              required: true
              type: string
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
                        user_id:
                            type: integer
                            example: 1
                        user_name:
                            type: string
                            example: user_1
                        followers:
                            type: array
                            items:
                                type: object
                                properties:
                                    id:
                                        type: integer
                                        example: 2
                                    name:
                                        type: string
                                        example: user_2
                        following:
                            type: array
                            items:
                                type: object
                                properties:
                                    id:
                                        type: integer
                                        example: 3
                                    name:
                                        type: string
                                        example: user_3
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
        logger.debug("Start get user in user")
        api_key = request.headers.get("api-key")
        if not api_key:
            logger.warning("User.post: no api-key provided")
            return {
                "result": False,
                "error_type": "missing_api_key",
                "error_message": "Не передан api-key",
            }, 401
        logger.debug("start crud user")
        try:
            user = crud_user_me(api_key=api_key)
            user_id = user.id
            user_name = user.name
            user_followers = user.followers
            user_following = user.following
            followers = [follow.follower_id for follow in user_followers]
            following = [follod.followed_id for follod in user_following]
            followers_response = []
            following_response = []
            if followers:
                for follower in followers:
                    data = {}
                    user = crud_user_id(user_id=follower)
                    data["id"] = user.id
                    data["name"] = user.name
                    followers_response.append(data)
            if following:
                for follow in following:
                    data = {}
                    user = crud_user_id(user_id=follow)
                    data["id"] = user.id
                    data["name"] = user.name
                    following_response.append(data)
            logger.debug("Finish get user in user")
            return jsonify(
                {
                    "result": True,
                    "user": {
                        "id": user_id,
                        "name": user_name,
                        "followers": followers_response,
                        "following": following_response,
                    },
                }
            )
        except UserNotFoundError:
            logger.warning("User.post: user not found error")
            return {
                "result": False,
                "error_type": "user_not_found",
                "error_message": "Пользователь не надйен",
            }, 404
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "result": False,
                "error_type": "internal_server_error",
                "error_message": "Внутренняя ошибка сервера",
            }, 500


class User(Resource):
    def get(self, user_id: int):
        """
        Получить информацию о любом пользователе
        ---
        tags:
            - UserId
        parameters:
            - name: user_id
              in: path
              required: true
              type: integer
              description: Уникальный id user
              example: 1
        responses:
            200:
                description: Успешный ответ
                schema:
                    type: object
                    properties:
                        result:
                            type: boolean
                            example: true
                        user_id:
                            type: integer
                            example: 3
                        user_name:
                            type: string
                            example: user_3
                        followers:
                            type: array
                            items:
                                type: object
                                properties:
                                    id:
                                        type: integer
                                        example: 2
                                    name:
                                        type: string
                                        example: user_2
                        following:
                            type: array
                            items:
                                type: object
                                properties:
                                    id:
                                        type: integer
                                        example: 3
                                    name:
                                        type: string
                                        example: user_3
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
        logger.debug("Start get user in user")
        try:
            logger.debug("Start get user_id")
            user = crud_user_id(user_id=user_id)
            user_followers = user.followers
            user_following = user.following
            followers = [follow.follower_id for follow in user_followers]
            following = [follod.followed_id for follod in user_following]
            followers_response = []
            following_response = []
            if followers:
                for follower in followers:
                    data = {}
                    followers_user = crud_user_id(user_id=follower)
                    data["id"] = followers_user.id
                    data["name"] = followers_user.name
                    followers_response.append(data)
            if following:
                for follow in following:
                    data = {}
                    followed_user = crud_user_id(user_id=follow)
                    data["id"] = followed_user.id
                    data["name"] = followed_user.name
                    following_response.append(data)
            logger.debug("Finish get user_id in user")
            return jsonify(
                {
                    "result": True,
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "followers": followers_response,
                        "following": following_response,
                    },
                }
            )
        except UserNotFoundError:
            logger.warning("User.post: user not found error")
            return {
                "result": False,
                "error_type": "user_not_found",
                "error_message": "Пользователь не надйен",
            }, 404
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "result": False,
                "error_type": "internal_server_error",
                "error_message": "Внутренняя ошибка сервера",
            }, 500


class UserFollow(Resource):
    def post(self, user_id: int):
        """
        Подписка на пользователя
        ---
        tags:
          - Users
        parameters:
          - name: api-key
            in: header
            required: true
            type: string
            description: API-ключ текущего пользователя
          - name: user_id
            in: path
            required: true
            type: integer
            description: ID пользователя, на которого нужно подписаться
            example: 3
        responses:
          200:
            description: Успешная подписка
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
          409:
            description: Конфликт — пользователь уже подписан
            schema:
              type: object
              properties:
                result:
                  type: boolean
                  example: false
                error_type:
                  type: string
                  example: "already_following"
                error_message:
                  type: string
                  example: "Вы уже подписаны на данного пользователя"
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
        logger.debug("Start follower in user")
        api_key = request.headers.get("api-key")
        if not api_key:
            logger.warning("User.post: no api-key provided")
            return {
                "result": False,
                "error_type": "missing_api_key",
                "error_message": "Не передан api-key",
            }, 401
        try:
            logger.debug("Start crud follower in user")
            crud_user_follower(api_key=api_key, user_id=user_id)
            logger.debug("Finish crud follower in user")
            return {
                "result": True,
            }, 201
        except UserNotFoundError:
            logger.warning("User.post: user not found error")
            return {
                "result": False,
                "error_type": "user_not_found",
                "error_message": "Пользователь не найден",
            }, 404
        except FollowNotFoundError:
            logger.warning("User.post: user not found error")
            return {
                "result": False,
                "error_type": "user in follower",
                "error_message": "Вы уже подписаны на данного user",
            }, 409
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "result": False,
                "error_type": "internal_server_error",
                "error_message": "Внутренняя ошибка сервера",
            }, 500

    def delete(self, user_id: int):
        """
        Отписка от пользователя
        ---
        tags:
          - Users
        parameters:
          - name: api-key
            in: header
            required: true
            type: string
            description: API-ключ текущего пользователя
          - name: user_id
            in: path
            required: true
            type: integer
            description: ID пользователя, от которого нужно отписаться
            example: 3
        responses:
          200:
            description: Успешная отписка
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
          409:
            description: Конфликт — пользователь не подписан
            schema:
              type: object
              properties:
                result:
                  type: boolean
                  example: false
                error_type:
                  type: string
                  example: "not_following"
                error_message:
                  type: string
                  example: "Вы не подписаны на данного пользователя"
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
        logger.debug("Start back follower in user")
        api_key = request.headers.get("api-key")
        if not api_key:
            logger.warning("User.post: no api-key provided")
            return {
                "result": False,
                "error_type": "missing_api_key",
                "error_message": "Не передан api-key",
            }, 401
        try:
            logger.debug("Start crud back follower in user")
            crud_delete_user_follow(api_key=api_key, user_id=user_id)
            logger.debug("Finish crud back follower in user")
            return {"result": True}
        except UserNotFoundError:
            logger.warning("User.post: user not found error")
            return {
                "result": False,
                "error_type": "user_not_found",
                "error_message": "Пользователь не найден",
            }, 404
        except FollowNotFoundError:
            logger.warning("User.post: user not found error")
            return {
                "result": False,
                "error_type": "user in follower",
                "error_message": "Вы не подписаны на данного user",
            }, 409
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "result": False,
                "error_type": "internal_server_error",
                "error_message": "Внутренняя ошибка сервера",
            }, 500
