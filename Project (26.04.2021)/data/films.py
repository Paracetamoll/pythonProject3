import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Films(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'films'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    director = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    duration = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    year = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    #img = sqlalchemy.Column(sqlalchemy.Binary, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
