from sqlalchemy import Table
from common.database import dbconnect

dbsession, md, DBase = dbconnect()


class Article():
    __table__ = Table('user', md, autoload='True')
