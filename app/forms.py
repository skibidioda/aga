from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import SubmitField, PasswordField, BooleanField
from wtforms.validators import Length, DataRequired, Email, EqualTo

from .models import Category


def get_categories():
    categories = Category.query.all()
    return [(category.id, category.title) for category in categories]


class NewsForm(FlaskForm):
    title = StringField("Название новости", validators=[DataRequired(message="Поле не должно быть пустым"),
                                                        Length(max=255,
                                                               message="Длинна должна быть не более 256 символов")])
    text = TextAreaField("Описание", validators=[DataRequired("Поле не должно быть пустым")])
    category = SelectField(choices=get_categories())
    submit = SubmitField("Добавить")


class LoginForm(FlaskForm):
    username = StringField('Юзернейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Юзернейм')
    name = StringField('Имя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message='Некорректный email')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    check_password = PasswordField('Подтвердите пароль',
                                   validators=[DataRequired(), EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField('Зарегистрироваться')
