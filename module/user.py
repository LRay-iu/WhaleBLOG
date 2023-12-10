import random
import time

from flask import session
from sqlalchemy import Column, Integer, String, DateTime
from main import app
from common.database import dbconnect

dbsession, DBase = dbconnect()


class User(DBase):
    __tableName__ = 'user'

    userid = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='用户唯一编号')
    username = Column(String(50), nullable=False, comment='用户名，邮箱')
    password = Column(String(32), nullable=False)
    nickname = Column(String(30), nullable=True)
    avatar = Column(String(20), nullable=False, comment='用户头像的图片文件名')
    role = Column(String(10), nullable=True, comment='用户角色')
    credit = Column(Integer, nullable=True, default=1000000, comment='整数类型，默认为1000，表示用户剩余积分')
    createTime = Column(DateTime, nullable=True, comment='数据新增时间')
    updateTime = Column(DateTime, nullable=True, comment='数据修改时间')

    # def __init__(self, username, password, nickname, avatar, role, credit, createTime, updateTime):
    #     super().__init__()
    #     self.username = username
    #     self.password = password
    #     self.nickname = nickname
    #     self.avatar = avatar
    #     self.role = role
    #     self.credit = credit
    #     self.createTime = createTime
    #     self.updateTime = updateTime

    def find_all(self):
        result = dbsession.query(User).all()
        print(result)
        return result

    # 查找用户是否以及注册
    def find_by_username(self, username):
        result = dbsession.query(User).filter_by(username=username).all()
        return result

    # 实现注册，首次注册时用户只需输入用户名和密码
    def do_register(self, username, nickname, password):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        avatar = str(random.randint(1, 15))
        user = User(username=username, password=password, role='user', nickname=nickname, avatar=avatar + '.png',
                    credit=1000000, createTime=now, updateTime=now)
        dbsession.add(user)
        dbsession.commit()
        return user

    # 修改用户剩余积分，积分为证书表示增加积分，为负数则表示减少积分
    def update_credit(self, credit):
        user = dbsession.query(User).filter_by(userid=session.get('userid')).one()
        user.credit = int(user.credit) + credit
        dbsession.commit()
