from flask import Blueprint, abort, render_template, request, session, jsonify

from module.article import Article
from module.comment import Comment
from module.credit import Credit
from module.user import User

comment = Blueprint("comment", __name__)


@comment.before_request
def before_comment():
    if session.get('islogin') is None or session.get('islogin') != 'true':
        return 'not-login'
    else:
        pass


@comment.route('/comment', methods=['POST'])
def add():
    articleid = request.form.get('articleid')
    content = request.form.get('content')
    # 请求里本身就有ip地址
    ipaddr = request.remote_addr
    # 对评论内容进行简单校验
    if len(content) < 5 or len(content) > 1000:
        return 'content-invalid'
    comment = Comment()
    if not comment.check_limit_per_20():
        try:
            comment.insert_comment(articleid, content, ipaddr)
            # 评论成功之后，更新积分明细和剩余积分，及文章回复数量
            Credit().insert_detail(type='添加评论', target=articleid, credit=2)
            User().update_credit(2)
            Article().update_replycount(articleid=articleid)
            return 'add-pass'
        except Exception as e:
            print(e)
            return 'add-fail'
    else:
        return 'add-limit'


@comment.route('/reply', methods=['POST'])
def reply():
    articleid = request.form.get('articleid')
    content = request.form.get('content')
    commentid = request.form.get('commentid')
    # 请求里本身就有ip地址
    ipaddr = request.remote_addr
    # 对评论内容进行简单校验
    if len(content) < 5 or len(content) > 1000:
        return 'content-invalid'
    comment = Comment()
    if not comment.check_limit_per_20():
        try:
            comment.insert_reply(articleid, commentid, content, ipaddr)
            # 评论成功之后，更新积分明细和剩余积分，及文章回复数量
            Credit().insert_detail(type='回复评论', target=articleid, credit=2)
            User().update_credit(2)
            Article().update_replycount(articleid=articleid)
            return 'add-pass'
        except Exception as e:
            print(e)
            return 'add-fail'
    else:
        return 'add-limit'

@comment.route('/comment/<int:articleid>-<int:page>')
def comment_page(articleid,page):
    start = (page-1)*10
    comment = Comment()
    list = comment.get_comment_user_list(articleid,start,10)
    return jsonify(list)
