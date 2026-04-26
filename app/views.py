from flask import render_template, redirect, url_for
from news import news_for_today
from . import app, db
from .models import News, Category
from .forms import NewsForm

@app.route('/', methods=["GET", "POST"])
def home_page():
    news_for_today = News.query.all()
    categories = Category.query.all()
    return render_template('index.html', news_for_today=news_for_today, categories=categories)

@app.route('/news')
def news_page():
    return "Новости"

@app.route('/add_news', methods=["GET", "POST"])
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        new_news = News()
        new_news.title = form.title.data
        new_news.text = form.text.data
        # button = form.button.data
        db.session.add(new_news)
        db.session.commit()
        # news_for_today.append({'title': title, 'text': text})
        return redirect(url_for('news_detail', id=new_news.id))
    categories = Category.query.all()
    return render_template('add_news.html', form=form, categories=categories)

@app.route('/news_detail/<int:news_id>')
def news_detail(news_id):
    # return f"Новость {news_id}"
    categories = Category.query.all()
    return render_template("news_detail.html", title=news_for_today[news_id]['title'],
                           text=news_for_today[news_id]['text'], categories=categories)

@app.route('/category/<int:id>')
def news_in_category(id):
    category = Category.query.get(id)
    news = category.news
    category_name = category.title
    categories = Category.query.all()
    return render_template('category.html', news=news, category_name=category_name, categories=categories)