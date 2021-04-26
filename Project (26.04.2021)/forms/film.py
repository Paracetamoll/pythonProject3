from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash


class FilmForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    year = StringField('Год', validators=[DataRequired()])
    genre = StringField('Жанр', validators=[DataRequired()])
    duration = StringField('Длительность', validators=[DataRequired()])
    director = StringField('Режиссер', validators=[DataRequired()])
    description = TextAreaField('Описание фильма', validators=[DataRequired()])
#    description = StringField('Описание фильма', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
