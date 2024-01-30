import re, hashlib

from flask import Blueprint, make_response, session, request, redirect, url_for, jsonify

from common.utility import *
from module.credit import Credit
from module.user import User, dbsession

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
    # en_username = encrypt_data(username,key)
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

key = 'abcdefghijklmnop'
# 新用户注册
@user.route('/user', methods=['POST'])
def register():
    user = User()
    username = request.form.get('username').strip()
    nickname = request.form.get('nickname').strip()
    password = request.form.get('password').strip()
    # en_username = encrypt_data(username,key)
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

@user.route('/change')
def dochange():
    user = User()
    users = user.find_all()
    for user in users:
        encrypted_username = encrypt_data(user.username,key)
        encrypted_nickname = encrypt_data(user.nickname,key)
        encrypted_role = encrypt_data(user.role,key)
        print (encrypted_username)
        print (encrypted_nickname)
        print (encrypted_role)
        user.username = encrypted_username
        user.nickname = encrypted_nickname
        user.role = encrypted_role
        dbsession.commit()
    return 'encrypted-done'

@user.route('/rechange')
def rechange():
    user = User()
    users = user.find_all()
    for user in users:
        decrypted_username = decrypt_data(user.username,key)
        decrypted_nickname = decrypt_data(user.nickname,key)
        decrypted_role = decrypt_data(user.role,key)
        print (decrypted_username)
        print (decrypted_nickname)
        print (decrypted_role)
        user.username = decrypted_username
        user.nickname = decrypted_nickname
        user.role = decrypted_role
        dbsession.commit()
    return 'decrypted-done'























