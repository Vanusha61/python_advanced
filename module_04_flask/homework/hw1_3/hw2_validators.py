"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""

from wtforms.validators import ValidationError
from flask_wtf import FlaskForm
from wtforms.fields import Field

def number_len(min_len: int, max_len: int, message = None):
    if message is None:
        message = f"Число должно содержать от {min_len} до {max_len} цифр"
    def number_length(form: FlaskForm, field: Field):
        if len(field.data) < min_len or len(field.data) > max_len:
            raise ValidationError(message)
    return number_length


class NumberLength:
    def __init__(self, min_len: int, max_len: int, message = None):
        self.min_len = min_len
        self.max_len = max_len
        self.message = message if message is not None else f"Число должно содержать от {min_len} до {max_len} цифр"

    def __call__(self, form: FlaskForm, field: Field):
        if len(field.data) < self.min_len or len(field.data) > self.max_len:
            raise ValidationError(self.message)