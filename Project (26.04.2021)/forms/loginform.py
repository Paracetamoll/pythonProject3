from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class ContactsForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    text = TextAreaField('Ваш отзыв', validators=[DataRequired()])
    submit = SubmitField('Отправить')
