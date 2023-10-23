from flask import Blueprint, render_template

from main import app
from module.article import Article

index = Blueprint("index", __name__)


@index.route('/')
def home():
    article = Article()
    result = article.find_limit_with_users(0, 10)
    print(result)
    return render_template('index.html')
@index.route('/ar')
def home2():
    print("hello")
    return render_template('article_user.html')
