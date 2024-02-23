# Создайте форму регистрации пользователей в приложении Flask. Форма должна
# содержать поля: имя, фамилия, email, пароль и подтверждение пароля. При отправке
# формы данные должны валидироваться на следующие условия:
# ○ Все поля обязательны для заполнения.
# ○ Поле email должно быть валидным email адресом.
# ○ Поле пароль должно содержать не менее 8 символов, включая хотя бы одну букву и
# одну цифру.
# ○ Поле подтверждения пароля должно совпадать с полем пароля.
# ○ Если данные формы не прошли валидацию, на странице должна быть выведена
# соответствующая ошибка.
# ○ Если данные формы прошли валидацию, на странице должно быть выведено
# сообщение об успешной регистрации.



from sqlalchemy.exc import OperationalError
from flask import Flask, render_template, redirect, url_for, flash
from models import db, User
from forms import RegForm, LoginForm

import random

app = Flask(__name__)
app.config['SECRET_KEY'] = b'418264e963f5167b8eb25425ce21c3b619950b9656199e98d7e96de6330699dc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

db.init_app(app)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('OK')


def result(message):
    return render_template('result.html', message=message)


@app.route('/')
@app.route('/registration/', methods=['GET', 'POST'])
@app.route('/task7/', methods=['GET', 'POST'])
def registration():
    form = RegForm()
    if form.validate_on_submit():
        is_error = False
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password: str = form.password.data
        if User.query.filter_by(email=email).first():
            is_error = True
            form.email.errors.append('Эта почта уже зарегистрирована!')
        if not any(char.isdigit() for char in password):
            is_error = True
            form.password.errors.append('В пароле должна быть хоть 1 цифра!')
        if not any(char.isupper() for char in password):
            is_error = True
            form.password.errors.append('В пароле должна быть хоть 1 заглавная буква!')
        if not is_error:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('registration.html', form=form, title='task7')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            return result("Добро пожаловать!")
        flash('Почта и/или пароль не подошли.', 'danger')
    return render_template('login.html', form=form, title='task7')


if __name__ == '__main__':
    app.run(debug=True)