from sqlalchemy import MetaData


def dbconnect():
    from main import db
    # 确保进程安全
    dbsession=db.session
    # 定义了一个数据库光标
    DBase=db.Model
    # 元数据，描述数据的数据
    metadata=MetaData(bind=db.engine)
    return (dbsession,metadata,DBase)