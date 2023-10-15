from flask import Flask, render_template, request, session, make_response
import os
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__, static_url_path='/', template_folder='template', static_folder='resource')
app.config['SECRET_KEY'] = os.urandom(24)  # 生成随机数种子

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:10181024@localhost:3306/whaleblog?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False  #跟踪数据库的修改，及时发送信号
#实例化db对象
db = SQLAlchemy(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_base.html')

@app.errorhandler(500)
def server_error(e):
    return render_template('500_base.html')

if __name__ == '__main__':
    from controller.index import *
    app.register_blueprint(index)

    app.run(debug=True, port=8080)
