from sqlalchemy import Column, Integer, String, DateTime
from main import app
from common.database import dbconnect
dbsession,DBase=dbconnect()
with app.app_context():
            class User(DBase):
                __tablename__ = 'user'

                userid = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='用户唯一编号')
                username = Column(String(50), nullable=False, comment='用户名，邮箱')
                password = Column(String(32), nullable=False)
                nickname = Column(String(30), nullable=True)
                avatar = Column(String(20), nullable=False, comment='用户头像的图片文件名')
                role = Column(String(10), nullable=True, comment='用户角色')
                credit = Column(Integer, nullable=True, default=1000000, comment='整数类型，默认为1000，表示用户剩余积分')
                createtime = Column(DateTime, nullable=True, comment='数据新增时间')
                updatetime = Column(DateTime, nullable=True, comment='数据修改时间')


                def __init__(self, username, password, nickname, avatar, role, credit):
                    super().__init__()
                    self.username = username
                    self.password = password
                    self.nickname = nickname
                    self.avatar = avatar
                    self.role = role
                    self.credit = credit

                def find_all(self):
                    result = db.session.query(User).all()
                    print(result)
                    return result
