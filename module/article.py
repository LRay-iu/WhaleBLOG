from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, func
from main import app
from common.database import dbconnect
from module.user import User

dbsession, DBase = dbconnect()


class Article(DBase):
    __tableName__ = 'article'
    articleid = Column(Integer, primary_key=True, autoincrement=True, comment='文章编号(唯一)')
    userid = Column(Integer, ForeignKey('user.userid'), comment='发布者')
    headline = Column(String(100), nullable=False, comment='标题，最长100')
    content = Column(Text, comment='文章内容')
    thumbnail = Column(String(20), comment='缩略图文件名')
    credit = Column(Integer, default=0, comment='阅读文章所需积分')
    readCount = Column(Integer, default=0, comment='阅读次数')
    replyCount = Column(Integer, default=0, comment='回复次数')
    recommended = Column(Boolean, default=False, comment='是否设置为推荐文章')
    hidden = Column(Boolean, default=False, comment='文章是否被隐藏')
    drafted = Column(Boolean, default=False, comment='文章是否为草稿')
    checked = Column(Boolean, default=True, comment='是否已被审核')
    createTime = Column(DateTime, comment='数据新增时间')
    updateTime = Column(DateTime, comment='数据修改时间')

    def find_all(self):
        row = dbsession.query(Article).all()
        return row

    # 返回包含用户以及文章对象的一个元组
    def find_by_id(self, articleid):
        row = dbsession.query(Article, User.nickname).join(User, User.userid == Article.userid).filter(
            Article.articleid == articleid).all()
        return row[0]

    # 不好的命名，但是想不到更好的了
    # 只返回文章对象
    def search_by_id(self, articleid):
        row = dbsession.query(Article).filter(Article.articleid == articleid).first()
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
        # SELECT *
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
        # print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))
        # result=query.all()
        return result

    # 统计分页总数量
    def get_count_by_headline(self, headline):
        count = dbsession.query(Article).filter(Article.hidden == 0,
                                                Article.drafted == 0,
                                                Article.checked == 1,
                                                Article.headline.like('%' + headline + '%'), ).count()
        return count

    # 最新文章
    def find_last_9(self):
        result = dbsession.query(Article.articleid, Article.headline). \
            filter(Article.hidden == 0,
                   Article.drafted == 0,
                   Article.checked == 1) \
            .order_by(Article.articleid.desc()).limit(9).all()
        return result

    # 最多阅读
    def find_most_9(self):
        result = dbsession.query(Article.articleid, Article.headline). \
            filter(Article.hidden == 0,
                   Article.drafted == 0,
                   Article.checked == 1) \
            .order_by(Article.readCount.desc()).limit(9).all()
        return result

    # 特别推荐
    def find_recommended_9(self):
        result = dbsession.query(Article.articleid, Article.headline). \
            filter(Article.hidden == 0,
                   Article.drafted == 0,
                   Article.checked == 1,
                   Article.recommended == 1) \
            .order_by(func.rand()).limit(9).all()
        return result

    # 一次性返回
    def find_last_most_recommended(self):
        last = self.find_last_9()
        most = self.find_most_9()
        recommended = self.find_recommended_9()
        return last, most, recommended

    # 阅读次数加一
    def update_read_count(self, articleid):
        article = self.search_by_id(articleid)
        # print(article.headline)
        if article:
            article.readCount += 1
            dbsession.commit()
            # print('阅读加一成功')
        else:
            print('查无文章')

    # 根据文章id查找文章标题
    def find_headline_by_id(self, articleid):
        row = dbsession.query(Article.headline).filter_by(articleid=articleid).first()
        return row.headline

    # 根据文章id查找上一篇和下一篇文章标题
    def find_prev_next_by_id(self, articleid):
        dict = {}
        # 寻找上一篇，原理是寻找文章编号小的序列中最大的一个
        row = dbsession.query(Article) \
            .filter(Article.hidden == 0,
                    Article.drafted == 0,
                    Article.checked == 1,
                    Article.articleid > articleid).order_by(Article.articleid).limit(1).first()

        if row is None:
            prev_id = articleid
        else:
            prev_id = row.articleid
        dict['prev_id'] = prev_id
        dict['prev_headline'] = self.find_headline_by_id(prev_id)
        # 寻找下一篇，原理是寻找文章编号大的序列中最小的一个
        row = dbsession.query(Article) \
            .filter(Article.hidden == 0,
                    Article.drafted == 0,
                    Article.checked == 1,
                    Article.articleid < articleid).order_by(Article.articleid.desc()).limit(1).first()
        if row is None:
            next_id = articleid
        else:
            next_id = row.articleid
        dict['next_id'] = next_id
        dict['next_headline'] = self.find_headline_by_id(next_id)
        return dict
