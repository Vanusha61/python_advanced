"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""


import subprocess

from flask import Flask, request
from wtforms.validators import DataRequired, NumberRange
from wtforms import StringField, IntegerField
from flask_wtf import FlaskForm

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    print("hello")
    return "Hello World!"


class CodeForm(FlaskForm):
    code = StringField(validators=[DataRequired(message="Код не передан")])
    timeout = IntegerField(
        default=5,
        validators=[
            NumberRange(min=1, max=30, message="Таймаут должен быть от 1 до 30 секунд")
        ]
    )


@app.route("/subprocess_api", methods=["POST"])
def subprocess_api():
    form = CodeForm()

    code = form.code.data
    timeout = form.timeout.data
    if not form.validate_on_submit():
        return {"errors": form.errors}, 400
    try:
        # "prlimit", "--nproc=1:1", "--cpu=30", "--as=100000000",
        cmd = ["python", "-c", code]
        res = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        stdout, stderr = res.communicate(timeout=timeout)
        return {
            "stdout": stdout,
            "stderr": stderr,
            "код_возврата": res.returncode
        }, 200
    except subprocess.TimeoutExpired:
        res.kill()
        stdout, stderr = res.communicate()
        return {
            "error": f"Выполнение прервано по таймауту {timeout} секунд",
            "частичный_вывод": stdout,
            "частичная_ошибка": stderr
        }, 408
    except Exception as e:
        return {"error": f"Ошибка выполнения: {str(e)}"}, 500


if __name__ == "__main__":
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(port=5000)
