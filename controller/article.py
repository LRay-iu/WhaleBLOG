from flask import Blueprint, abort, render_template, request

from module.article import Article
from module.credit import Credit
from module.favorite import Favorite
from module.user import User

article = Blueprint("article", __name__)


@article.route('/article/<int:articleid>')
def read(articleid):
    # 数据格式(<Article 47>, 'anqixu704')
    result = Article().find_by_id(articleid)
    print(result)
    if result is None:
        abort(404)
    print(result[0])
    # 文章内容减半
    dict = {}
    for k, v in result[0].__dict__.items():
        if not k.startswith('_sa_instance_state'):
            dict[k] = v
    dict['nickname'] = result.nickname
    position = 0
    payed = Credit().check_payed_article(articleid)
    if not payed:
        content = dict['content']
        temp = content[0:int(len(content) / 2)]
        if '</p>' in temp:
            position = temp.rindex('</p>') + 4
            dict['content'] = temp[0:position]
        else:
            # 如果无法找到 '</p>'，可以根据实际情况设置默认的 position 值或执行其他逻辑
            position = len(content) // 2
            dict['content'] = temp
            dict['content'] = temp[0:position]
    try:
        # 找不到文章抛出异常404
        Article().update_read_count(articleid)
        is_favorite = Favorite().check_favorite(articleid)
        prev_next = Article().find_prev_next_by_id(articleid)
        return render_template('article_user.html',
                               article=dict, position=position, payed=payed,
                               is_favorite=is_favorite, prev_next=prev_next)
    except Exception as e:
        print(e)
        abort(500)


@article.route('/readall', methods=['POST'])
def read_all():
    position = int(request.form.get('position'))
    print(position)
    articleid = request.form.get('articleid')
    article = Article()
    result = article.find_by_id(articleid)
    content = result[0].content[position:]
    # 添加积分明细
    Credit().insert_detail(type='阅读文章', target=articleid, credit=-1 * result[0].credit)
    # 扣除用户表剩余积分
    User().update_credit(credit=-1 * result[0].credit)
    return content
