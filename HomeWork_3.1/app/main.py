# Flask-SQLAlchemy

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect


from app.models import db, User
from app.forms import RegisterForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# инициализация БД
db.init_app(app)

app.config['SECRET_KEY'] = b'ea000bc6bbd140100d66503aa6ac1242c6eb0e8d4c38b85c7ea9a9d2a8e60451'
# получение csrf - объекта для работы с формами
csrf = CSRFProtect(app)



@app.route('/')
def index():
    return render_template('base.html')


@app.cli.command("init-db")
def init_db():
    # создать все таблицы
    db.create_all()
    # print('OK')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data

        # получить user из БД по name и email
        # можно через filter-by (только AND ???? )
        existing_user = User.query.filter((User.name == name) | (User.surname == surname) | (User.email == email)).first()

        # если user существует
        if existing_user:
            error_msg = 'Username or surname or email уже существует.'
            form.name.errors.append(error_msg)
            return render_template('register.html', form=form)

        user = User(name=name, surname=surname, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return 'Регистрация успешно пройдена!'
    return render_template('register.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)