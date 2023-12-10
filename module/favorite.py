import time
from datetime import datetime

from flask import session
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean

from common.database import dbconnect

dbsession, DBase = dbconnect()


class Favorite(DBase):
    __tablename__ = 'favorite'

    favoriteid = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='收藏表编号')
    articleid = Column(Integer, ForeignKey('article.articleid', ondelete='CASCADE'), nullable=False,
                       comment='关联文章表信息')
    userid = Column(Integer, ForeignKey('user.userid', ondelete='CASCADE'), nullable=False, comment='关联用户表信息')
    canceled = Column(Boolean, default=False, comment='文章是否被取消收藏')
    createTime = Column(DateTime, nullable=True, comment='新增时间', default=datetime.utcnow)
    updateTime = Column(DateTime, nullable=True, comment='修改时间', default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    def insert_favorite(self, articleid):
        row = dbsession.query(Favorite).filter_by(articleid=articleid, userid=session.get('userid')).first()
        if row is not None:
            row.canceled = 0
        else:
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            favorite = Favorite(articleid=articleid, userid=session.get('userid'), canceled=0, createTime=now,
                                updateTime=now)
            dbsession.add(favorite)
        dbsession.commit()

    # 取消收藏
    def cancel_favorite(self, articleid):
        row = dbsession.query(Favorite).filter_by(articleid=articleid, userid=session.get('userid')).first()
        row.canceled = 1
        dbsession.commit()

    def check_favorite(self, articleid):
        row = dbsession.query(Favorite).filter_by(articleid=articleid, userid=session.get('userid')).first()
        if row is None:
            return False
        elif row.canceled==1:
            return False
        else:
            return True
