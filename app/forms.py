from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import Length, DataRequired
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
    button = SubmitField("Добавить")
