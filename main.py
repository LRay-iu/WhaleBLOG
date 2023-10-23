from flask import Flask, render_template, request, session, make_response
import os
from flask_sqlalchemy import SQLAlchemy
import pymysql



app = Flask(__name__, static_url_path='/', template_folder='template', static_folder='resource')
app.config['SECRET_KEY'] = os.urandom(24)  # 生成随机数种子
pymysql.install_as_MySQLdb()   #ModuleNotFoundError:"No module named "MySQLdb"
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:10181024@localhost:3306/whaleblog?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False  #跟踪数据库的修改，及时发送信号
#实例化db对象
from common.database import db
db.init_app(app)#在database中初始化，在main.py中注册

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



