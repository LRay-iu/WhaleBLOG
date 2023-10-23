from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
def dbconnect():

    # 确保进程安全
    dbsession = db.session
    # 定义了一个数据库光标
    DBase = db.Model
    return (dbsession, DBase)