from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import FileField


class MediaForm(FlaskForm):
    file = FileField(
        "file",
        validators=[
            FileRequired(message="Файл не загружен"),
            FileAllowed(
                ["jpg", "jpeg", "png", "gif"],
                message="Разрешены только изображения (jpg, jpeg, png, gif)",
            ),
        ],
    )
