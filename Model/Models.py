# encoding: utf-8
"""
@auth: cyq
@file: models.py
@desc: 模型
"""
import time

import jwt
from flask import current_app, abort
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
    def assertName(cls, name):
        res = cls.query.filter_by(name=name).first()
        if res:
            abort(400, f"已存在  {name}!")

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
            abort(500, f"err:{e}")

    def Delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            log.exception(e)
            db.session.rollback()
            abort(500, f"err:{e}")

    def delete(self):
        self.status = self.DELETE_STATUS
        try:
            db.session.commit()
        except Exception as e:
            log.exception(e)
            abort(500, f"err:{e}")


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

    interface = db.relationship("Interfaces", backref="project_interface", lazy='dynamic')
    case = db.relationship('Case', backref="project_case", lazy='dynamic')
    ucase = db.relationship("UICase", backref='project_ucase', lazy='dynamic')
    method = db.relationship("UMethod", backref='project_method', lazy='dynamic')
    debugtalk = db.relationship("DebugTalks", backref='project_debugtalk', uselist=False)

    def __init__(self, name, desc):
        self.project_desc = desc
        self.project_name = name

    def __repr__(self):
        return f"project_name:{self.project_name}"

    @classmethod
    def assertIdExisted(cls, id):
        p = cls.query.get(id)
        if not p:
            abort(400, f"projectId {id} 不存在或删除")
        return p

    @classmethod
    def assertName(cle, name):
        res = cle.query.filter_by(project_name=name).first()
        if res:
            abort(400, "projectName 重复!")

    def delete(self):
        self.status = self.DELETE_STATUS
        # 级联修改状态
        for interface in self.interfaces_records:
            interface.status = self.DELETE_STATUS
            for case in interface.case_records:
                case.status = self.DELETE_STATUS
        db.session.commit()

    # debugtalk
    @property
    def debugtalk_records(self):
        return self.debugtalks.filter_by().first()

    # interfaces动态属性
    @property
    def interfaces_records(self):
        return self.interface.filter_by().all()


# debugtalks
class DebugTalks(Base):
    __tablename__ = 'debugtalks'
    name = db.Column(db.String(200), default="debugtalk.py", comment="debugtalk文件名称")
    debugtalks = db.Column(db.TEXT, nullable=True, default='#debugtalk.py', comment='debugtalk.py文件')
    project = db.Column(db.Integer, db.ForeignKey("project.id"))

    def __repr__(self):
        return f"{self.id}"


# 接口
class Interfaces(Base):
    __tablename__ = "interfaces"
    interface_name = db.Column(db.String(32), nullable=False, comment="接口名")
    interface_desc = db.Column(db.String(500), default="", comment='描述')
    tester = db.Column(db.String(32), comment='测试人')

    project_id = db.Column(db.INT, db.ForeignKey("project.id"))
    case = db.relationship("Case", backref="interface", lazy="dynamic")

    def __init__(self, name, desc, pid):
        self.interface_desc = desc
        self.interface_name = name
        self.project_id = pid

    @classmethod
    def assertName(cle, name):
        res = cle.query.filter_by(interface_name=name).first()
        if res:
            abort(400, f"interface_name 重复!")

    @classmethod
    def assertIdExisted(cls, id):
        p = cls.query.get(id)
        if not p or p.status == 0:
            abort(400, "interface 不存在或删除")

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
        return f"Interfaces:{self.interface_name}"


# 環境
class Envs(Base):
    __tablename__ = 'envs'
    name = db.Column(db.String(200), unique=True, comment="测试环境名称")
    base_url = db.Column(db.String(200), comment="请求URL")
    desc = db.Column(db.String(200), nullable=True, default="")

    @classmethod
    def assertIdExisted(cls, id):
        p = cls.query.get_or_NoFound(id)
        if not p or p.status == 0:
            abort(400, "envId 不存在或删除")
        return p

    def delete(self):
        self.status = self.DELETE_STATUS
        try:
            self.status = self.DELETE_STATUS
            db.session.commit()
        except Exception as e:
            log.exception(e)
            db.session.rollback()

    def __init__(self, name, url, desc):
        self.name = name
        self.base_url = url
        self.desc = desc

    def __repr__(self):
        return f"name:{self.name}"


# 用例
class Case(Base):
    __tablename__ = "case"
    type = db.Column(db.SmallInteger, default=1, comment="做扩展")
    name = db.Column(db.String(32), nullable=False, unique=True, comment="用例名称")
    desc = db.Column(db.String(32), nullable=True, comment="desc")
    request = db.Column(db.TEXT, comment="测试数据")

    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), comment="用例項目")
    interface_id = db.Column(db.INT, db.ForeignKey("interfaces.id"), comment="用例的接口")
    author = db.Column(db.String(32), default="", comment="创建者")

    pwd = db.Column(db.String(200), nullable=True, comment="测试：报告地址")

    def __init__(self, name, request, pid=None, project_id=None, interface_id=None, author=None, desc=None):
        self.name = name
        self.request = request
        self.project_id = project_id
        self.desc = desc
        self.author = author
        self.interface_id = interface_id
        self.project_id = pid

    @property
    def getInterfaceInfo(self):
        interface = Interfaces.query.get(self.interface_id)
        return interface

    @property
    def getProjectInfo(self):
        p = Project.query.get(self.project_id)
        return p

    @classmethod
    def assertName(cls, name):
        res = cls.query.filter_by(name=name).first()
        if res:
            abort(400, "caseName 重复!")

    def __repr__(self):
        return f"name:{self.name}"


class Report(Base):
    __tablename__ = "report"
    name = db.Column(db.String(200), unique=True, comment="测试报告")
    result = db.Column(db.Boolean, default=False, comment="测试结果")
    count = db.Column(db.Integer, nullable=True, comment="用例数")
    success = db.Column(db.Integer, nullable=True, comment="成功数")
    html = db.Column(db.TEXT, default="", comment="报告html")
    summary = db.Column(db.TEXT, default="", comment="报告详情")

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


# UIcaseDemo
class UICase(Base):
    __tablename__ = 'uicase'
    name = db.Column(db.String(200), unique=False, comment="用例名称")
    desc = db.Column(db.String(200), nullable=True, default="", comment="用例描述")
    creator = db.Column(db.String(20), comment="创建人")

    headless = db.Column(db.Boolean, default=False, comment="是否无头测试,默认false")
    windowsSize = db.Column(db.String(20), default="1920,1080", nullable=True, comment="窗口大小")

    # (stay,running,over)
    state = db.Column(db.String(32), default="stay", comment="实时状态")

    casesteps = db.relationship("Steps", backref="uicase", cascade='all,delete')

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), comment='项目Id')

    def __init__(self, name: str, creator: str, project_id: str, desc=None, headless=None,
                 windowsSize=None):
        self.name = name
        self.desc = desc
        self.project_id = project_id
        self.creator = creator
        self.headless = headless
        if windowsSize:
            self.windowsSize = windowsSize

    def delete_steps(self):
        try:
            for step in self.steps_records:
                db.session.delete(step)
                db.session.commit()
        except Exception as e:
            log.exception(e)
            db.session.rollback()

    @property
    def steps_records(self):
        return self.casesteps

    @property
    def get_steps_info(self):

        info = []
        for step in self.casesteps:
            data = {}
            data['stepId'] = step.id
            data['name'] = step.name
            data['desc'] = step.desc
            data['is_method'] = step.is_method
            data['type'] = step.type
            data['log'] = step.log
            data['locator'] = step.locator
            data['do'] = step.do
            data['value'] = step.value
            data['variable'] = step.variable
            data['validate'] = step.validate
            data['pic'] = step.pic
            data['data'] = step.data
            info.append(data)
        data = {"caseId": self.id,
                'caseName': self.name,
                'caseDesc': self.desc,
                "caseCreator": self.creator,
                "Headless": self.headless,
                "windowsSize": self.windowsSize,
                "state": self.state,
                "status": self.status,
                "PorjectId": self.project_id,
                "caseSteps": info}
        return data

    def __repr__(self):
        return f"name:{self.name}"


DO = ['click', 'get', 'send_keys', 'get_text', 'get_title', 'get_url', 'clear', 'action_click', 'action_send_keys',
      'switch_window', 'go_back', 'screenshot', 'js', 'sleep']


class Steps(Base):
    __tablename__ = 'steps'
    case_id = db.Column(db.Integer, db.ForeignKey('uicase.id'), nullable=True, comment='所属用例')
    name = db.Column(db.String(200), nullable=True, unique=False, comment="步骤名称")
    desc = db.Column(db.String(200), nullable=True, comment="步骤描述")
    is_method = db.Column(db.Integer, nullable=True, comment="方法")
    type = db.Column(db.String(32), nullable=True, comment="步骤类型")
    log = db.Column(db.String(100), nullable=True, comment="这步骤日志")
    locator = db.Column(db.String(100), nullable=True, comment="步骤元素")
    do = db.Column(db.String(32), nullable=True, comment='步驟操作')
    value = db.Column(db.TEXT, nullable=True, comment="请求数据")
    variable = db.Column(db.TEXT, nullable=True, comment="变量名称")
    validate = db.Column(db.TEXT, nullable=True, comment="认证")
    pic = db.Column(db.String(100), nullable=True, comment="截圖地址")
    data = db.Column(db.String(100), nullable=True, comment="验证数据")

    def __init__(self, name=None, desc=None, is_method=None, type=None, locator=None, do=None,
                 value=None, variable=None, validate=None):
        self.name = name
        self.desc = desc
        self.is_method = is_method
        self.type = type
        self.locator = locator
        if do:
            do = self.assertDo(do)
        else:
            do = do
        self.do = do
        self.value = value
        self.variable = variable
        self.validate = validate

    def assertDo(self, do: str) -> abort:
        if do not in DO:
            abort(400, f"Parameter:{do} not support")
        return do

    def __repr__(self):
        return f"name:{self.name}"


class UMethod(Base):
    __tablename__ = 'umethod'
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), comment="項目Id")
    name = db.Column(db.String(200), unique=True, comment="方法名称")
    desc = db.Column(db.String(200), nullable=True, comment="方法描述")
    body = db.Column(db.TEXT, comment="步骤step")
    creator = db.Column(db.String(20), comment="创建人")
    updater = db.Column(db.String(20), comment="修改人")

    def __init__(self, pid, name, body, creator, desc=""):
        self.project_id = pid
        self.name = name
        self.desc = desc
        self.body = body
        self.creator = creator

    def __repr__(self):
        return f"name:{self.name}"
