from sqlalchemy import Table

from common.database import dbconnect

dbsession, md, DBase = dbconnect()


class User(DBase):
    __table__ = Table('user', md, autoload='True')
    def find_all(self):
        result=dbsession.query(user).all()
        print(result)
        return result