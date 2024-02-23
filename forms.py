from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField('Электронная почта', validators=[Email()])
    password = PasswordField('Пароль', validators=[Length(min=6, max=20)])
    repeat_password = PasswordField('Подтверждение пароля', validators=[EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[Email()])
    password = PasswordField('Пароль', validators=[Length(min=6, max=20)])
    submit = SubmitField('Войти')