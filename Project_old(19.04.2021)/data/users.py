import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)

'''
{% extends "base.html" %}

{% block content %}
{{ super() }}
<style>
   form {
    margin-left: 20px;
   }
</style>
<body bgcolor="#FFFAFA">
<form action="" method="post">
    <h1>Авторизация</h1>
    {{ form.hidden_tag() }}
    <p>
        {{ form.email.label }}<br>
        {{ form.email(class="form-control", type="email") }}<br>
        {% for error in form.email.errors %}
            <p class="alert alert-danger" role="alert">
                {{ error }}
            </p>
        {% endfor %}
    </p>
    <p>
        {{ form.password.label }}<br>
        {{ form.password(class="form-control", type="password") }}<br>
        {% for error in form.password.errors %}
            <p class="alert alert-danger" role="alert">
                {{ error }}
            </p>
        {% endfor %}
    </p>
    <p>
        {{ form.password_again.label }}<br>
        {{ form.password_again(class="form-control", type="password") }}<br>
        {% for error in form.password_again.errors %}
            <p class="alert alert-danger" role="alert">
                {{ error }}
            </p>
        {% endfor %}
    </p>
    <p>
        {{ form.name.label }}<br>
        {{ form.name(class="form-control") }}<br>
        {% for error in form.name.errors %}
            <p class="alert alert-danger" role="alert">
                {{ error }}
            </p>
        {% endfor %}
    </p>
    <p>
        {{ form.about.label }}<br>
        {{ form.about(class="form-control") }}<br>
        {% for error in form.about.errors %}
            <p class="alert alert-danger" role="alert">
                {{ error }}
            </p>
        {% endfor %}
    </p>
    <p>{{ form.submit(type="submit", class="btn btn-primary") }}</p>
    {{message}}
</form>
{% endblock %}
</body>'''