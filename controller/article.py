import math

from flask import Blueprint, abort, render_template, request, session

from common.utility import parse_image_url, generate_thumb
from module.article import Article
from module.comment import Comment
from module.credit import Credit
from module.favorite import Favorite
from module.user import User

article = Blueprint("article", __name__)


@article.route('/article/<int:articleid>')
def read(articleid):
    # 数据格式(<Article 47>, 'anqixu704')
    result = Article().find_by_id(articleid)
    # print(result)
    if result is None:
        abort(404)
    # print(result[0])
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
        # 获取当前文章的上一页和下一页
        prev_next = Article().find_prev_next_by_id(articleid)
        # 获取当前文章对应的评论
        comment_user = Comment().find_limit_with_user(articleid, 0, 10)
        print('comment_user')
        # print(comment_user)
        comment_list = Comment().get_comment_user_list(articleid, 0, 50)
        # print(comment_list)
        comment_count = Comment().get_count_by_article(articleid)
        total = math.ceil(comment_count / 10)
        return render_template('article_user.html',
                               article=dict, position=position, payed=payed,
                               is_favorite=is_favorite, prev_next=prev_next, comment_list=comment_list, total=total)
    except Exception as e:
        print('文章报错')
        print(e)
        abort(500)


@article.route('/readall', methods=['POST'])
def read_all():
    position = int(request.form.get('position'))
    articleid = request.form.get('articleid')
    article = Article()
    result = article.find_by_id(articleid)
    content = result[0].content[position:]
    # 添加积分明细
    Credit().insert_detail(type='阅读文章', target=articleid, credit=-1 * result[0].credit)
    # 扣除用户表剩余积分
    User().update_credit(credit=-1 * result[0].credit)
    return content


@article.route('/prepost')
def pre_post():
    return render_template('post_user.html')


@article.route('/article', methods=['POST'])
def add_article():
    headline = request.form.get('headline')
    content = request.form.get('content')
    credit = int(request.form.get('credit'))
    drafted = int(request.form.get('drafted'))
    checked = int(request.form.get('checked'))
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        user = User().find_by_userid(session.get('userid'))
        if user[0].role == 'editor' or 'admin':
            # 权限合格
            url_list = parse_image_url(content)
            if len(url_list) > 0:
                thumbname = generate_thumb(url_list)
            else:
                thumbname = 'index.png'
            try:
                id = Article().insert_article(headline=headline, content=content, credit=credit,thumbnail=thumbname,drafted=drafted,checked=checked)
                return str(id)
            except Exception as e:
                print(e)
                return 'post-fail'
        #角色不是作者，只能投稿，不能正式发布
        elif checked == 1:
            return 'perm-denied'
        else:
            return 'perm-denied'
