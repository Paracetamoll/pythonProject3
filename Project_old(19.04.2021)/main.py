from flask import Flask, url_for, render_template, redirect
from data import db_session

from data.users import User
from data.films import Films
from forms.user import RegisterForm
from forms.loginform import LoginForm
from flask_login import login_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    db_session.global_init("db/filmoteka.db")
    db_sess = db_session.create_session()

    return render_template("index.html") #, res=res)


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
    #res = []
    #print(film_id)
    film = db_sess.query(Films).filter((Films.id == film_id)).first()
    return render_template("view.html", film=film)


@app.route('/auto', methods=['GET', 'POST'])
def auto():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('auto.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('auto.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('auto.html', title='Регистрация', form=form)
    # return render_template("auto.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    '''
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    '''
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/contacts')
def contacts():
    return render_template("contacts.html")


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
