from requests import get, post, delete

print(get('http://localhost:5000/api/film/1').json())
print(get('http://localhost:5000/api/film/2').json())
print(get('http://localhost:5000/api/film/3').json())
print(post('http://localhost:5000/api/films_create',
           json={'title': 'qwq',
                 'director': 'David',
                 'description': 'None',
                 'genre': 'боевик',
                 'duration': '12',
                 'year': '1998'}).json())
print(get('http://localhost:5000/api/film/17').json())
print(delete('http://localhost:5000/api/films_delete/999').json())
print(delete('http://localhost:5000/api/films_delete/17').json())

