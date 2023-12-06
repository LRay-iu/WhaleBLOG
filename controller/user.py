import re, hashlib

from flask import Blueprint, make_response, session, request, redirect, url_for

from common.utility import *
from module.credit import Credit
from module.user import User

user = Blueprint("user", __name__)


@user.route('/vcode')
def vcode():
    code, bstring = imageCode().get_code()
    print(code)
    response = make_response(bstring)
    response.headers['Content-Type'] = 'image/jpeg'
    session['vcode'] = code.lower()
    return response


# 发送邮件的部分
# 发送验证码
@user.route('/ecode', methods=['POST'])
def ecode():
    email = request.form.get('email')
    if not re.match('.+@.+\..+', email):
        return 'email-invalid'
    code = gen_email_code()
    print(code)
    try:
        send_email(email, code)
        session['ecode'] = code
        return 'send-pass'
    except:
        return 'send-fail'


# 用户登录模块
@user.route('/login', methods=['POST'])
def login():
    user = User()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    vcode = request.form.get('vcode').lower().strip()
    # 校验图形验证码是否正确
    if vcode != session.get('vcode'):
        return 'vcode-error'
    # 万能验证码，使用postman进行调试时可以解开注释
    # if vcode != '0000':
    #     return 'vcode-error'
    else:
        # 实现登录
        password = hashlib.md5(password.encode()).hexdigest()
        result = user.find_by_username(username)
        if len(result) == 1 and result[0].password == password:
            session['islogin'] = 'true'
            session['userid'] = result[0].userid
            session['username'] = result[0].username
            session['nickname'] = result[0].nickname
            session['role'] = result[0].role
            # 更新积分详情表
            Credit().insert_detail(type='正常登录', target='0', credit=1)
            user.update_credit(1)
            #将Cookie写入浏览器
            response=make_response('log-pass')
            response.set_cookie('username',username,max_age=30*24*3600)
            response.set_cookie('password',password,max_age=30*24*3600)
            return response
        else:
            return 'log-fail'


# 新用户注册
@user.route('/user', methods=['POST'])
def register():
    user = User()
    username = request.form.get('username').strip()
    nickname = request.form.get('nickname').strip()
    password = request.form.get('password').strip()
    ecode = request.form.get('ecode').strip()
    if ecode != session.get('ecode'):
        return 'ecode-error'
    elif not re.match('.+@.+\..+', username) or len(password) < 5:
        return 'up-invalid'
    elif len(user.find_by_username(username)) > 0:
        return 'up-exist'
    else:
        # 实现注册
        password = hashlib.md5(password.encode()).hexdigest()
        result = user.do_register(username, nickname, password)
        session['islogin'] = 'true'
        session['userid'] = result.userid
        session['username'] = result.username
        session['nickname'] = result.nickname
        session['role'] = result.role
        # 更新积分详情表
        Credit().insert_detail(type='用户注册', target='0', credit=1000000)
        return 'reg-pass'
#用户注销
@user.route('/logout')
def logout():
    #清空session，页面跳转
    session.clear()
    response=make_response('注销并进行重定向',302)
    response.headers['Location']=url_for('index.home')
    response.delete_cookie('username')
    response.set_cookie('password','',max_age=0)
    # response.delete_cookie('password')
    return response



























