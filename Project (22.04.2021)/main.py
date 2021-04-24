from flask import Flask, url_for, request, render_template, redirect, flash
from data import db_session

from data.users import User
from data.films import Films
from forms.user import RegisterForm
from forms.film import FilmForm
from forms.loginform import LoginForm
from flask_login import login_user
from flask_login import LoginManager
from flask_login import login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    db_session.global_init("db/filmoteka.db")
    db_sess = db_session.create_session()

    return render_template("index.html")


@app.route('/catalog')
def catalog():
    db_session.global_init("db/filmoteka.db")
    db_sess = db_session.create_session()
    res = []
    for film in db_sess.query(Films).order_by(Films.title).all():
        res.append([film.title, film.year, film.genre, film.duration, film.director, film.description[0:30] + "...", film.id])
    return render_template("catalog.html", res=res)


@app.route('/view/<film_id>')
def view(film_id):
    db_session.global_init("db/filmoteka.db")
    db_sess = db_session.create_session()
    film = db_sess.query(Films).filter((Films.id == film_id)).first()
    return render_template("view.html", film=film)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            nickname=form.nickname.data,
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/contacts')
def contacts():
    form = LoginForm()
    return render_template("contacts.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/film_add', methods=['GET', 'POST'])
@login_required
def film_add():
    db_session.global_init("db/filmoteka.db")
    db_sess = db_session.create_session()
    form = FilmForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        film = Films(
            title=form.title.data,
            year=form.year.data,
            genre=form.genre.data,
            duration=form.duration.data,
            director=form.director.data,
            description=form.description.data
        )

        db_sess.add(film)
        db_sess.commit()
        flash('Фильм "' + film.title + '" добавлен в каталог')
        return redirect('/catalog')

    return render_template("film_add.html", form=form)


@app.route('/film_delete/<film_id>', methods=['GET', 'POST'])
@login_required
def film_delete(film_id):
    db_session.global_init("db/filmoteka.db")
    db_sess = db_session.create_session()
    film = db_sess.query(Films).filter(Films.id == film_id).first()
    title = film.title
    db_sess.delete(film)
    db_sess.commit()
    flash('Фильм "' + film.title + '" удален из каталога')
    return redirect('/catalog')


@app.route('/film_edit/<film_id>', methods=['GET', 'POST'])
@login_required
def film_edit(film_id):
    db_session.global_init("db/filmoteka.db")
    db_sess = db_session.create_session()
    form = FilmForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        '''
        if db_sess.query(Films).filter(Films.id == film_id).first():
            
            film1 = Films(
                title=form.title.data,
                year=form.year.data,
                genre=form.genre.data,
                duration=form.duration.data,
                director=form.director.data,
                description=form.description.data
            )
            

            print(film1.title, film1.year, film1.genre, film1.duration, film1.director, film1.description)
            db_sess.commit()
        
        '''
        film = db_sess.query(Films).filter(Films.id == film_id).first()

        print(form.title.data, type(form.title.data),
              form.year.data,  type(form.year.data),
              form.genre.data, type(form.genre.data),
              form.duration.data, type(form.duration.data),
              form.director.data,  type(form.director.data),
              form.description.data, type(form.description.data))


        if film:
            film.title=form.title.data
            film.year=form.year.data
            film.genre=form.genre.data
            film.duration=form.duration.data
            film.director=form.director.data
            film.description=form.description.data
            print(film.title, film.year, film.genre, film.duration, film.director, film.description)

            db_sess.commit()
            return redirect('/view/' + film_id)

    film = db_sess.query(Films).filter((Films.id == film_id)).first()
    return render_template("film_edit.html", film=film, form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            nickname=form.nickname.data,
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        #db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('profile.html', title='Профиль', form=form)
    # return render_template("auto.html")


'''
@app.route('/profile/<user_id>', methods=['GET', 'POST'])
@login_required
def profile_id(user_id):

    db_session.global_init("db/filmoteka.db")
    db_sess = db_session.create_session()
    form = FilmForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        film = db_sess.query(Films).filter(Films.id == film_id).first()

        print(form.title.data, type(form.title.data),
              form.year.data,  type(form.year.data),
              form.genre.data, type(form.genre.data),
              form.duration.data, type(form.duration.data),
              form.director.data,  type(form.director.data),
              form.description.data, type(form.description.data))
        if film:
            film.title=form.title.data
            film.year=form.year.data
            film.genre=form.genre.data
            film.duration=form.duration.data
            film.director=form.director.data
            film.description=form.description.data
            print(film.title, film.year, film.genre, film.duration, film.director, film.description)

            db_sess.commit()
            return redirect('/view/' + film_id)
    user = db_sess.query(User).filter((User.id == user_id)).first()
    return render_template("profile.html", user=user, form=form)
'''














@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/form_sample', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                        </style>
                            <title>Пример формы</title>
                          </head>
                          <body>
                            <h1>Форма для регистрации в суперсекретной системе</h1>
                            <div>
                                <form class="login_form" method="post">
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <input type="password" class="form-control" id="password" placeholder="Введите пароль" name="password">
                                    <div class="form-group">
                                        <label for="classSelect">В каком вы классе</label>
                                        <select class="form-control" id="classSelect" name="class">
                                          <option>7</option>
                                          <option>8</option>
                                          <option>9</option>
                                          <option>10</option>
                                          <option>11</option>
                                        </select>
                                     </div>
                                    <div class="form-group">
                                        <label for="about">Немного о себе</label>
                                        <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                                    </div>
                                    <div class="form-group">
                                        <label for="photo">Приложите фотографию</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>
                                    <div class="form-group">
                                        <label for="form-check">Укажите пол</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                          <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">
                                            Женский
                                          </label>
                                        </div>
                                    </div>
                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                        <label class="form-check-label" for="acceptRules">Готов быть добровольцем</label>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Записаться</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        print(request.form['email'])
        print(request.form['password'])
        print(request.form['class'])
        print(request.form['file'])
        print(request.form['about'])
        print(request.form['accept'])
        print(request.form['sex'])
        return "Форма отправлена"


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
