from flask import Flask, render_template, request, session, make_response
import os
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__, static_url_path='/', template_folder='template', static_folder='resource')
app.config['SECRET_KEY'] = os.urandom(24)  # 生成随机数种子
pymysql.install_as_MySQLdb()  # ModuleNotFoundError:"No module named "MySQLdb"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:10181024@localhost:3306/whaleblog?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 跟踪数据库的修改，及时发送信号
# 实例化db对象
from common.database import db

db.init_app(app)  # 在database中初始化，在main.py中注册


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_base.html')


@app.errorhandler(500)
def server_error(e):
    return render_template('500_base.html')


def mytruncate(s, length, end='...'):
    # 中文定义为一个字符，英文为0.5个字符
    # 遍历整个字符串，获取到每一个字符的ASCII码，如果是（0-127或256），则认为是英文，否则当作中文处理
    count = 0
    new = ''
    if len(s) <= 14:
        end = ''
    for c in s:
        new += c  # 每循环一次，添加一个字符到n
        if ord(c) <= 128:
            count += 0.5
        else:
            count += 1
        if count > length:
            break
    return new + end


@app.before_request
def before():
    from module.user import User
    url = request.path
    pass_list = ['/user', '/login', '/logout']
    if url in pass_list or url.endswith('.js') or url.endswith('.jpg'):
        pass
    elif session.get('islogin') is None:
        username = request.cookies.get('username')
        password = request.cookies.get('password')
        if username != None and password != None:
            user = User()
            result = user.find_by_username(username)
            if len(result) == 1 and result[0].password == password:
                session['islogin'] = 'true'
                session['userid'] = result[0].userid
                session['username'] = result[0].username
                session['nickname'] = result[0].nickname
                session['role'] = result[0].role


# 注册mytruncate过滤器
app.jinja_env.filters.update(mytruncate=mytruncate)

if __name__ == '__main__':
    from controller.index import *
    app.register_blueprint(index)

    from controller.user import *
    app.register_blueprint(user)

    from controller.article import *
    app.register_blueprint(article)

    from controller.favorite import *
    app.register_blueprint(favorite)

    app.run(debug=True, port=8080)
