from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from main import app
from common.database import dbconnect
from module.user import User

dbsession, DBase = dbconnect()
with (app.app_context()):
    class Article(DBase):
        __tablename__ = 'article'
        articleid = Column(Integer, primary_key=True, autoincrement=True, comment='文章编号(唯一)')
        userid = Column(Integer, ForeignKey('user.userid'), comment='发布者')
        headline = Column(String(100), nullable=False, comment='标题，最长100')
        content = Column(Text, comment='文章内容')
        thumbnail = Column(String(20), comment='缩略图文件名')
        credit = Column(Integer, default=0, comment='阅读文章所需积分')
        readcount = Column(Integer, default=0, comment='阅读次数')
        replycount = Column(Integer, default=0, comment='回复次数')
        recommended = Column(Boolean, default=False, comment='是否设置为推荐文章')
        hidden = Column(Boolean, default=False, comment='文章是否被隐藏')
        drafted = Column(Boolean, default=False, comment='文章是否为草稿')
        checked = Column(Boolean, default=True, comment='是否已被审核')
        createtime = Column(DateTime, comment='数据新增时间')
        updatetime = Column(DateTime, comment='数据修改时间')

        def find_all(self):
            row = dbsession.query(Article).all()
            return row

        def find_by_id(self, articalid):
            row = dbsession.query(Article).filter_by(articalid).first()
            return row

        # 指定分页的limit和offset的参数值，同时与与用户表做连接查询
        def find_limit_with_users(self, start, count):
            # select * from article inner join User on user.userid = article.userid order by article.articleid desc limit count offset start
            result = dbsession.query(Article, User).join(User, User.userid == Article.userid) \
                .filter(Article.hidden == 0,
                        Article.drafted == 0,
                        Article.checked == 1) \
                .order_by(Article.articleid.desc()).limit(count).offset(start).all()
            return result

        # 统计文章总数量
        def get_total_count(self):
            count = dbsession.query(Article).filter(Article.hidden == 0,
                                                    Article.drafted == 0,
                                                    Article.checked == 1).count()
            return count

        # 根据文章标题进行模糊搜索
        def find_by_headline(self, headline, start, count):
            #SELECT *
            # FROM article JOIN user ON article.userid = user.userid
            # WHERE article.hidden = 0 AND article.drafted = 0 AND article.checked = 1 AND article.headline LIKE '%s%' ORDER BY article.articleid DESC
            #  LIMIT 5 OFFSET 0
            result = dbsession.query(Article, User).join(User, User.userid == Article.userid) \
                .filter(Article.hidden == 0,
                        Article.drafted == 0,
                        Article.checked == 1,
                        Article.headline.like('%' + headline + '%')) \
                .order_by(
                Article.articleid.desc()).limit(count).offset(start).all()
            #print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))
            #result=query.all()
            return result

        # 统计分页总数量
        def get_count_by_headline(self, headline):
            count = dbsession.query(Article).filter(Article.hidden == 0,
                                                    Article.drafted == 0,
                                                    Article.checked == 1,
                                                    Article.headline.like('%' + headline + '%'),).count()
            return count
