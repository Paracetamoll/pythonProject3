from requests import get, post, delete


# Получение информации о фильме по id
print(get('http://localhost:5000/api/film/1').json())
print(get('http://localhost:5000/api/film/2').json())
print(get('http://localhost:5000/api/film/3').json())

# Получение полного списка всех фильмов
print(get('http://localhost:5000/api/films').json())

# Получение информации о фильме по его названию
print(get('http://localhost:5000/api/film_by_title/Афоня').json())

# Добавление в каталог нового фильма
print(post('http://localhost:5000/api/films_create',
           json={'title': 'Новый фильм',
                 'director': 'Новый режиссер',
                 'description': 'Новое описание',
                 'genre': 'Драма',
                 'duration': '90',
                 'year': '1985'}).json())

# Удаление информации о фильме по его id
print(delete('http://localhost:5000/api/films_delete/999').json())
print(delete('http://localhost:5000/api/films_delete/17').json())
