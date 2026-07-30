"""
В эндпоинт /registration добавьте все валидаторы, о которых говорилось в последнем видео:

1) email (текст, обязательно для заполнения, валидация формата);
2) phone (число, обязательно для заполнения, длина — десять символов, только положительные числа);
3) name (текст, обязательно для заполнения);
4) address (текст, обязательно для заполнения);
5) index (только числа, обязательно для заполнения);
6) comment (текст, необязательно для заполнения).
"""

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from hw2_validators import number_len, NumberLength

app = Flask(__name__)


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[Email(message="Невалидный email"), InputRequired(message="Ошибка, пустой email")])
    phone = StringField('phone', validators=[InputRequired(message="Ошибка, пустой phone"), Regexp(
        r"^\+?\d{10}$", message="Телефон должен содержать ровно 10 цифр (только числа)")]
                         )
    name = StringField('name', validators=[InputRequired(message="Ошибка, пустой name")])
    address = StringField('address', validators=[InputRequired(message="Ошибка, пустой address")])
    index = IntegerField('index', validators=[InputRequired(message="Ошибка, пустой index"),NumberRange(min=0, message="Индекс должен быть положительным числом")])
    comment = StringField('comment')

@app.route("/registration/", methods=["POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return jsonify({
            "email": form.email.data,
            "phone": f"+7{form.phone.data}",
            "name": form.name.data,
            "address": form.address.data,
            "index": form.index.data,
            "comment": form.comment.data
        }), 200

    return jsonify(form.errors), 400

if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
