# encoding: utf-8
"""
@auth: cyq
@name: dbOpt
@desc: 多数据库操作
"""
from FlaskDemo import app, db

SQLALCHEMY_DATABASE_URL = "sqlite:///tmp/test.db"  # 链接数据库
SQLALCHEMY_BINDS = "x"  # 一个映射绑定,(bind) 键到sqlacher
SQLALCHEMY_ECHO = True  # SQLALCHEMY 将会帮助
SQLALCHEMY_RECORD_QUERIES = "x"  # y可以用与显示禁用或者启用查询记录
SQLALCHEMY_POOL_SIZE = '123'  # 连接池设置大小
SQLALCHEMY_POOL_TIMEOUT = ';123'  # 数据库超时时间
SQLALCHEMY_ROOL_RECYCLE = 123  # 自动回收链接描述

app.config['SQLALCHEMY_BINDS'] = {
    "user": 'sqlite:xxx',
    "main": "mysql+pymysql:root:@localhost",
    "other": "xx"
}

"""
@command:

flask db init
flask db migrate 生成脚本
flask db upgrade 更新到数据库
flask db downgrade 退回 

@ormCommand

db.session.add(user)
db.session.add_all([user])

"""


# 多对一
class Project(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    modules = db.relationship("Module", backref='project')


class Module(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))


# 多对多
choiceClass = db.Table("choice",
                       db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
                       db.Column("sub_id", db.Integer, db.ForeignKey('subject.ud'))
                       )


class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(32))
    subjects = db.relationship("Subject", secondary=choiceClass, backref=db.backref("users", lazy="dynamic"))
    """
    lazy 默认懒加载 select
    user = User.query.get(1)
    user.subjects  ==> [Subject()实例]
    
    dynamic
    user = User.query.get(1)
    user.subjects  ==> query 对象
    
    """


class Subject(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(32))


def insert():
    user1 = User(name="t1")
    user2 = User(name="t2")

    subject1 = Subject(name='s1')
    subject2 = Subject(name='s2')

    user1.subjects.append(subject1)
    user2.subjects.append(subject2)
    db.session.add_all([user1,user2,subject1,subject2])

