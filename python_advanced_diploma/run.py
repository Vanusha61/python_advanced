import logging.config

from flasgger import Swagger
from flask import Flask, request, send_from_directory
from flask_restful import Api
from werkzeug.utils import secure_filename
from pathlib import Path

from app.api.tweets_api import TweetDelete, TweetLike, Tweets
from app.api.user_api import User, UserFollow, UserMe
from app.extensions import dict_config_api
from app.models.crud.media_crud import UserNotFound, crud_create_media
from app.schemas.media_schema import MediaForm

logging.config.dictConfig(dict_config_api)
logger = logging.getLogger("api_logger")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="dist",
    static_url_path="",
)

app.config["WTF_CSRF_ENABLED"] = False

api = Api(app)


@app.route("/")
@app.route("/login")
@app.route("/<path:filename>")
def index():
    return send_from_directory("dist", "index.html")


@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/api/medias", methods=["POST"])
def medias():
    """
    Загрузка медиафайла (картинки)
    ---
    tags:
      - Media
    parameters:
      - name: api-key
        in: header
        required: true
        type: string
        description: API-ключ пользователя
      - name: file
        in: formData
        required: true
        type: file
        description: Загружаемый файл (изображение)
    responses:
      200:
        description: Файл успешно загружен
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: true
            media_id:
              type: integer
              example: 5
      400:
        description: Ошибка валидации формы (неверный файл)
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: false
            error_type:
              type: string
              example: "invalid_request"
            errors:
              type: object
              description: Детали ошибок валидации
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
            errors:
              type: string
              example: "Пользователь не найден"
      500:
        description: Ошибка при сохранении файла или внутренняя ошибка
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: false
            error_type:
              type: string
              example: "upload_failed"
            error_message:
              type: string
              example: "Не удалось сохранить медиа"
    """
    logger.debug("starting media creation")
    api_key = request.headers.get("api-key")
    if not api_key:
        logger.warning("Media.post: no api-key provided")
        return {
            "result": False,
            "error_type": "missing_api_key",
            "error_message": "Не передан api-key",
        }, 401
    try:
        form = MediaForm()
        logger.debug("start media form")
        if form.validate():
            logger.debug("true media form")
            file = form.file.data
            filename = secure_filename(file.filename)
            file_path = UPLOAD_DIR / filename
            file.save(file_path)
            media = crud_create_media(
                api_key=api_key, file_path=f"/media/{filename}"
            )
            if media is None:
                return {
                    "result": False,
                    "error_type": "upload_failed",
                    "error_message": "Не удалось сохранить медиа",
                }, 500
            logger.debug("media creation crud")
            return {
                "result": True,
                "media_id": media.id,
            }
        logger.warning("false media form")
        return {
            "result": False,
            "error_type": "invalid_request",
            "errors": form.errors,
        }
    except UserNotFound:
        logger.warning("User not found")
        return {
            "result": False,
            "error_type": "user_not_found",
            "errors": "Пользователь не найден",
        }
    except Exception as err:
        logger.error(err)
        return {
            "result": False,
            "error_type": "internal_server_error",
            "error_message": "Внутренняя ошибка сервера",
        }, 500


api.add_resource(User, "/api/users/<int:user_id>")
api.add_resource(UserMe, "/api/users/me")
api.add_resource(UserFollow, "/api/users/<int:user_id>/follow")
api.add_resource(Tweets, "/api/tweets")
api.add_resource(TweetDelete, "/api/tweets/<int:tweet_id>")
api.add_resource(TweetLike, "/api/tweets/<int:tweet_id>/likes")

swagger = Swagger(app)

if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
