from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class FormAddBook(FlaskForm):
    book_title = StringField('book_title', validators=[DataRequired(message="Укажите поле Book Title")])
    author_name = StringField('author_name', validators=[DataRequired(message="Укажие поле Author Title")])
