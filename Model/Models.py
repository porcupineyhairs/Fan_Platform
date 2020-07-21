# encoding: utf-8
"""
@auth: cyq
@file: models.py
@desc: 模型
"""
import time

import jwt
from flask import current_app
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash

from App import db
from comments.log import get_log

log = get_log(__name__)


class Base(db.Model):
    DELETE_STATUS = 0

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.Integer, default=int(time.time()))
    update_time = db.Column(db.Integer, default=int(time.time()), onupdate=int(time.time()))
    status = db.Column(db.SmallInteger, default=1)

    @classmethod
    def all(cls):
        return cls.query.filter_by().order_by(desc(cls.id)).all()

    @classmethod
    def get(cls, id):
        return cls.query.get_or_NoFound(id)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            log.exception(e)
            db.session.rollback()


    def delete(self):
        self.status = self.DELETE_STATUS
        try:
            db.session.commit()
        except Exception as e:
            log.exception(e)


# 用戶
class User(Base):
    __tablename__ = 'user'
    username = db.Column(db.String(32), unique=True, index=True, comment="用户名")
    password = db.Column(db.String(128))
    email = db.Column(db.String(52), nullable=True, unique=False)
    phone = db.Column(db.String(12), unique=False, nullable=True)
    gender = db.Column(db.Boolean, default=True, nullable=True)  # 1 男 2 女
    admin = db.Column(db.Boolean, default=False)

    # 所属部门
    part = db.Column(db.Integer, db.ForeignKey("part.id"), nullable=True)

    def __init__(self, username, password, phone=None, email=None, partId=None, admin=None, gender=None):
        self.username = username
        self.part = partId
        self.admin = admin
        self.email = email
        self.gender = gender
        self.phone = phone
        self.hash_password(password)

    def get_userId(self):
        return self.id

    def is_superuser(self):
        return self.admin

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expires_in=30):
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return f"username:{self.username}"


# 部门
class Part(Base):
    __tablename__ = 'part'
    Part_Name = db.Column(db.String(32), unique=True)
    Part_Users = db.relationship("User", backref="user_part", lazy="dynamic")

    def __init__(self, partName):
        self.Part_Name = partName

    def __repr__(self):
        return f"part:{self.Part_Name}"


# project
class Project(Base):
    __tablename__ = "project"
    project_name = db.Column(db.String(32), nullable=False, default="", unique=True)
    project_desc = db.Column(db.String(500), nullable=False, default="")
    module = db.relationship("Module", backref="project", lazy='dynamic')

    def __init__(self, name, desc):
        self.project_desc = desc
        self.project_name = name

    def __repr__(self):
        return f"project_name:{self.project_name}"

    def delete(self):
        self.status = self.DELETE_STATUS
        # 级联修改状态
        for module in self.module_records:
            module.status = self.DELETE_STATUS
            for case in module.case_records:
                case.status = self.DELETE_STATUS
        db.session.commit()

    # 添加一个动态属性
    @property
    def module_records(self):
        return self.module.filter_by().all()


# 接口
class Module(Base):
    __tablename__ = "module"
    module_name = db.Column(db.String(32), nullable=False, comment="接口名")
    module_desc = db.Column(db.String(500), default="")

    project_id = db.Column(db.INT, db.ForeignKey("project.id"))
    case = db.relationship("Case", backref="module", lazy="dynamic")

    def __init__(self, name, desc, pid):
        self.module_desc = desc
        self.module_name = name
        self.project_id = pid


    def delete(self):
        self.status = self.DELETE_STATUS
        try:
            for case in self.case_records:
                case.status = self.DELETE_STATUS
            db.session.commit()
        except Exception as e:
            log.exception(e)
            db.session.rollback()


    @property
    def case_records(self):
        return self.case.filter_by().all()

    def __repr__(self):
        return f"module_name:{self.module_name}"


# 用例
class Case(Base):
    __tablename__ = "case"
    type = db.Column(db.SmallInteger, default=1, comment="做扩展")
    name = db.Column(db.String(32), nullable=False, comment="用例名称")
    include = db.Column(db.String(512), comment="可能存在子用例")
    request = db.Column(db.TEXT, comment="测试数据")
    module_id = db.Column(db.INT, db.ForeignKey("module.id"), comment="用例的接口")

    def __repr__(self):
        return f"name:{self.name}"


# 测试套件
class Suite(Base):
    """
    与用例多对多关系
    """
    __tablename__ = 'suite'
    name = db.Column(db.String(32))
    includes = db.Column(db.TEXT, comment="套件里的用例")

    def __repr__(self):
        return f"name:{self.name}"
