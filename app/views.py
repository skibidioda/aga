from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from . import app, db
from .forms import NewsForm, RegistrationForm, LoginForm
from .models import News, Category, User


@app.route('/', methods=["GET", "POST"])
def home_page():
    news_for_today = News.query.all()
    categories = Category.query.all()
    return render_template('index.html', news_for_today=news_for_today, categories=categories)


@app.route('/news')
def news_page():
    return "Новости"


@app.route('/add_news', methods=["GET", "POST"])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        new_news = News()
        new_news.title = form.title.data
        new_news.text = form.text.data
        new_news.category_id = form.category.data
        # button = form.button.data
        db.session.add(new_news)
        db.session.commit()
        flash("Регистрация прошла успешно!", 'alert-success')
        # news_for_today.append({'title': title, 'text': text})
        return redirect(url_for('news_detail', news_id=new_news.id))
    categories = Category.query.all()
    return render_template('add_news.html', form=form, categories=categories)


@app.route('/news_detail/<int:news_id>')
def news_detail(news_id):
    # return f"Новость {news_id}"
    news = News.query.get(news_id)
    categories = Category.query.all()
    return render_template("news_detail.html", news=news, categories=categories)


@app.route('/category/<int:id>')
def news_in_category(id):
    category = Category.query.get(id)
    news = category.news
    category_name = category.title
    categories = Category.query.all()
    return render_template('category.html', news=news, category_name=category_name, categories=categories)

@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.name = form.name.data
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Вход выполнен!", 'alert-success')
            return redirect(url_for('home_page'))
        else:
            flash("Не удалось войти", 'alert-danger')
    return render_template('login.html', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))