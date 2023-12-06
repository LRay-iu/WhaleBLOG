import time
from datetime import datetime

from flask import session
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from main import app
from common.database import dbconnect
from module.user import User

dbsession, DBase = dbconnect()
with app.app_context():
    class Credit(DBase):
        __tablename__ = 'credit'

        creditid = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='积分表编号')
        userid = Column(Integer, ForeignKey('user.userid', ondelete='CASCADE'), nullable=False)
        category = Column(String(10), nullable=False, comment='积分变化原因说明')
        target = Column(Integer, comment='积分来源或对象')
        credit = Column(Integer, comment='具体积分数量，可正可负')
        createTime = Column(DateTime, nullable=True, comment='新增时间', default=datetime.utcnow)
        updateTime = Column(DateTime, nullable=True, comment='修改时间', default=datetime.utcnow,
                            onupdate=datetime.utcnow)

        # 定义与 User 表的关联关系，通过userid与User表建立关联
        user = relationship("User", backref="credits")

        # def __init__(self, creditid, userid, category, target, credit, createTime, updateTime):
        #     super().__init__()
        #     self.creditid = creditid
        #     self.userid = userid
        #     self.category = category
        #     self.target = target
        #     self.credit = credit
        #     self.createTime = createTime
        #     self.updateTime = updateTime

        def __repr__(self):
            return f"Credit(creditid={self.creditid}, userid={self.userid}, category='{self.category}', ...)"

        def find_all(self):
            result = dbsession.query(Credit).all()
            print(result)
            return result

        # 插入积分明细数据
        def insert_detail(self, type, target, credit):
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            credit = Credit(userid=session.get('userid'), category=type, target=target,
                            credit=credit, createTime=now, updateTime=now)
            dbsession.add(credit)
            dbsession.commit()

