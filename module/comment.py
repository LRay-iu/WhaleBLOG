import time
from datetime import datetime

from flask import session
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, Text, String
from sqlalchemy.orm import relationship

from common.database import dbconnect
from common.utility import model_join_list
from module.user import User

dbsession, DBase = dbconnect()


class Comment(DBase):
    __tablename__ = 'comment'

    commentid = Column(Integer, primary_key=True, autoincrement=True, comment='评论编号')
    userid = Column(Integer, ForeignKey('user.userid', ondelete='SET NULL'), comment='关联评论者信息')
    articleid = Column(Integer, ForeignKey('article.articleid', ondelete='CASCADE'), nullable=False,
                       comment='文章表信息')
    content = Column(Text, comment='评论内容')
    ipaddr = Column(String(30), comment='用户IP地址')
    replyid = Column(Integer, comment='保存被回复的评论ID，原始评论值为0')
    agreeacount = Column(Integer, default=0, comment='点赞数')
    opposement = Column(Integer, default=0, comment='点踩数')
    hidden = Column(Integer, default=0, comment='评论是否被隐藏')
    createTime = Column(DateTime, comment='新增时间')
    updateTime = Column(DateTime, comment='修改时间')

    user = relationship("User")  # 声明与用户表关联的关系
    article = relationship("Article")  # 声明与文章表关联的关系

    # 新增一条评论
    def insert_comment(self, articleid, content, ipaddr):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        comment = Comment(userid=session.get('userid'), articleid=articleid, content=content, ipaddr=ipaddr,
                          createTime=now, updateTime=now)
        dbsession.add(comment)
        dbsession.commit()

    # 根据文章id查找所有评论
    def find_by_articleid(self, articleid):
        result = dbsession.query(Comment).filter_by(articleid=articleid, hidden=0, replyid=0).all()
        return result

    # 根据用户id和日期进行查询是否已经超过了每天5条的限制
    def check_limit_per_20(self):
        start = time.strftime('%Y-%m-%d 00:00:00')  # 每天起始时间
        end = time.strftime('%Y-%m-%d 23:59:59')  # 每天结束时间
        result = dbsession.query(Comment).filter(Comment.userid == session.get('userid'),
                                                 Comment.createTime.between(start, end)).all()
        if len(result) >= 20:
            return True
        else:
            return False

    def find_limit_with_user(self, articleid, start, count):
        result = dbsession.query(Comment, User).join(User, User.userid == Comment.userid).filter(
            Comment.articleid == articleid, Comment.hidden == 0, Comment.replyid == None).order_by(
            Comment.commentid.desc()).limit(count).offset(
            start).all()
        return result

    def insert_reply(self, articleid, commentid, content, ipaddr):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        comment = Comment(userid=session.get('userid'), articleid=articleid, content=content, ipaddr=ipaddr,
                          replyid=commentid, createTime=now, updateTime=now)
        dbsession.add(comment)
        dbsession.commit()

    def find_comment_with_user(self, articleid, start, count):
        result = dbsession.query(Comment, User).join(User, User.userid == Comment.userid) \
            .filter(Comment.hidden == 0,
                    Comment.articleid == articleid,
                    Comment.replyid == None).order_by(Comment.commentid.desc()).limit(count).offset(start).all()
        return result

    def find_reply_with_user(self, replyid):
        result = dbsession.query(Comment, User).join(User, User.userid == Comment.userid).filter(
            Comment.replyid == replyid, Comment.hidden == 0).all()
        return result

    def get_comment_user_list(self, articleid, start, count):
        result = self.find_comment_with_user(articleid, start, count)
        comment_list = model_join_list(result)
        for comment in comment_list:
            result = self.find_reply_with_user(comment['commentid'])
            comment['reply_list'] = model_join_list(result)
        return comment_list

    def get_count_by_article(self, articleid):
        count = dbsession.query(Comment).filter(Comment.articleid == articleid, Comment.replyid == None).count()
        return count
