import math

from flask import Blueprint, render_template, abort, jsonify

from main import app
from module.article import Article

index = Blueprint("index", __name__)


@index.route('/')
def home():
    article = Article()
    result = article.find_limit_with_users(0, 5)
    print(result)
    last,most,recommended=article.find_last_most_recommended()
    # 向上取整页数
    total = math.ceil(article.get_total_count() / 5)
    return render_template('index.html', result=result, total=total, page=1,
                           last=last,most=most,recommended=recommended)


@index.route('/page/<int:page>')
def paginate(page):
    start = (page - 1) * 5
    article = Article()
    result = article.find_limit_with_users(start, 5)
    # print(result)
    # 向上取整页数
    total = math.ceil(article.get_total_count() / 5)
    return render_template('index.html', result=result, total=total, page=page)


@index.route('/search/<int:page>-<keyword>')
def search(page, keyword):
    keyword=keyword.strip()
    if keyword is None or keyword=='' or '%' in keyword:
        abort(404)
    start = (page - 1) * 5
    article=Article()
    result=article.find_by_headline(keyword,start,5)
    total = math.ceil(article.get_count_by_headline(keyword)/5)
    return render_template('search.html',result=result,page=page,total=total,keyword=keyword)

@index.route('/recommend')
def recommend():
    article = Article()
    last,most,recommended=article.find_last_most_recommended()
    # 假设 last、most 和 recommended 是数据库查询返回的具有键值对的列表
    # last_dict = list(last)
    last_list = [list(item) for item in last]
    most_list = [list(item) for item in most]
    recommended_list = [list(item) for item in recommended]
    # list=[]
    # list.append(last_dict)
    # list.append(most_dict)
    # list.append(recommended_dict)
    data = {
        "test":[1,2,3,4,5],
        "last": last_list,
        "most": most_list,
        "recommended": recommended_list
    }
    return jsonify(data)