import flask
from flask import jsonify, request

from . import db_session
from .films import Films

blueprint = flask.Blueprint(
    'films_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/films')
def get_films():
    db_sess = db_session.create_session()
    films = db_sess.query(Films).all()
    return jsonify(
        {
            'films':
                [item.to_dict(only=('id', 'title', 'director', 'genre', 'duration', 'year', 'description'))
                 for item in films]
        }
    )


@blueprint.route('/api/film/<int:film_id>', methods=['GET'])
def get_one_film(film_id):
    db_sess = db_session.create_session()
    films = db_sess.query(Films).get(film_id)
    if not films:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'film': films.to_dict(only=(
                'id', 'title', 'director', 'genre', 'duration', 'year', 'description'))
        }
    )


#  пока не работает
@blueprint.route('/api/film_by_title/<string:film_title>', methods=['GET'])
def get_one_film_by_title(film_title):
    db_sess = db_session.create_session()
    print(film_title)
    films = db_sess.query(Films).filter(Films.title == film_title).first()
    print(films)
    if not films:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'films': films.to_dict(only=(
                'title', 'director', 'genre', 'duration', 'year', 'description'))
        }
    )


@blueprint.route('/api/films_create', methods=['POST'])
def create_news():
    print(request.json)
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'director', 'description', 'genre', 'duration', 'year']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    news = Films(
        title=request.json['title'],
        director=request.json['director'],
        description=request.json['description'],
        genre=request.json['genre'],
        duration=request.json['duration'],
        year=request.json['year']
    )
    db_sess.add(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/films_delete/<int:film_id>', methods=['DELETE'])
def delete_news(film_id):
    db_sess = db_session.create_session()
    films = db_sess.query(Films).get(film_id)
    if not films:
        return jsonify({'error': 'Not found'})
    db_sess.delete(films)
    db_sess.commit()
    return jsonify({'success': 'OK'})

