import math

from flask import Blueprint, render_template

from main import app
from module.article import Article

index = Blueprint("index", __name__)


@index.route('/')
def home():
    article = Article()
    result = article.find_limit_with_users(0, 5)
    print(result)
    # 向上取整页数
    total = math.ceil(article.get_total_count()/5)
    return render_template('index.html', result=result,total=total,page=1)


@index.route('/page/<int:page>')
def paginate(page):
    start = (page - 1) * 5
    article = Article()
    result = article.find_limit_with_users(start, 5)
    print(result)
    # 向上取整页数
    total = math.ceil(article.get_total_count()/5)
    return render_template('index.html', result=result,total=total,page=page)
