#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:muji
# datetime:2019/8/1 14:25
import json
import time

from flask import current_app
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash

from app.errors.exceptions import DatabaseException

login_manager = LoginManager()
# 配置登陆的视图函数
login_manager.login_view = 'web.login'


class MyBaseQuery(BaseQuery):
    def filter_by(self, **kwargs):
        kwargs.setdefault('status', 1)
        return super().filter_by(**kwargs)


db = SQLAlchemy(query_class=MyBaseQuery)


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.SmallInteger, default=1, nullable=False)
    created_at = db.Column(db.Integer, default=int(time.time()))
    updated_at = db.Column(db.Integer, default=int(time.time()), onupdate=int(time.time()))

    # 删除状态
    DELETE_STATUS = 0
    # 没激活状态
    INACTIVE_STATUS = 2

    @classmethod
    def all(cls):
        """查询所有记录，按创建的倒序排"""
        return cls.query.filter_by().order_by(desc(cls.id)).all()

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def paginate(cls, page=1, **filter_by):
        """分页展示"""
        per_page = current_app.config.get('PER_PAGE', 10)
        return cls.query.filter_by(**filter_by).order_by(desc(cls.updated_at)).paginate(
            int(page), per_page=per_page, error_out=False)


class ProjectInfo(Base):
    project_name = db.Column(db.String(64), unique=True, nullable=False)
    simple_desc = db.Column(db.String(512), default='')
    modules = db.relationship('ModuleInfo', backref='project', lazy='dynamic')

    @classmethod
    def add_by_form(cls, form):
        """添加项目"""
        p = cls(
            project_name=form.project_name.data,
            simple_desc=form.simple_desc.data,
        )
        try:
            db.session.add(p)
            db.session.commit()
            return p
        except Exception as e:
            current_app.logger.error('添加项目错误')
            raise e

    @classmethod
    def delete(cls, id):
        """TODO: 删除项目下面所有的module 和 cases, suites"""
        project = cls.query.get(int(id))
        project.status = cls.DELETE_STATUS
        try:
            db.session.add(project)
            db.session.commit()
            return project
        except Exception as e:
            raise DatabaseException('数据库操作异常，请联系管理员')

    def edit_by_form(self, form):
        """修改项目"""
        self.project_name = form.project_name.data
        self.simple_desc = form.simple_desc.data
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            current_app.logger.error('修改项目错误')
            raise DatabaseException('数据库操作异常，请联系管理员')

    @property
    def module_records(self):
        return self.modules.filter_by().all()


class ModuleInfo(Base):
    module_name = db.Column(db.String(20), nullable=False)
    simple_desc = db.Column(db.String(512), default='')
    project_id = db.Column(db.INT, db.ForeignKey('project_info.id'))
    test_cases = db.relationship('CaseInfo', backref='module', lazy='dynamic')

    @classmethod
    def add_by_form(cls, form):
        p = cls(
            module_name=form.module_name.data,
            simple_desc=form.simple_desc.data,
            project_id=int(form.project_id.data),
        )
        try:
            db.session.add(p)
            db.session.commit()
            return p
        except Exception as e:
            raise e

    def edit_by_form(self, form):
        self.module_name = form.module_name.data
        self.simple_desc = form.simple_desc.data
        self.project_id = int(form.project_id.data)
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            raise e

    @classmethod
    def delete(cls, id):
        """
        TODO: 删除接口下面所有的 cases, suites
        :param id:
        :return:
        """
        module = cls.query.get(int(id))
        module.status = cls.DELETE_STATUS
        try:
            db.session.add(module)
            db.session.commit()
            return module
        except Exception as e:
            raise e

    @property
    def case_records(self):
        return self.test_cases.filter_by().all()


class CaseInfo(Base):
    type = db.Column(db.SmallInteger, default=1)
    name = db.Column(db.String(20), nullable=False)
    include = db.Column(db.String(512))
    request = db.Column(db.Text)  # 所有的测试数据 json, yaml.loads()
    module_id = db.Column(db.INT, db.ForeignKey('module_info.id'))

    @classmethod
    def delete(cls, id):
        case = cls.query.get(int(id))
        case.status = cls.DELETE_STATUS
        try:
            db.session.add(case)
            db.session.commit()
            return case
        except Exception as e:
            raise e

    @staticmethod
    def transact_validate(data):
        """validate 格式"""
        key = data.pop('key', '')
        value = data.pop('value', '')
        data.setdefault('check', key)
        data.setdefault('expect', value)
        return data

    @classmethod
    def case_info_by_form(cls, form):
        """通过 form 数据验证保存 case"""
        request_datas = form.get("request_datas", {}).pop('test', {})
        headers = form.get("headers", {}).pop('test', {})
        jsons = form.get("json_datas", {}).pop('test', {})
        extracts = form.get('extracts', {}).pop('test', {})
        hooks = form.get('hooks', {}).pop('test', {})
        parameters = form.get('parameters', {}).pop('test', {})
        validates = form.get('validates', {}).pop('test', [])
        variables = form.get('variables', {}).pop('test', {})

        # [{"key":"username" ,"value":"yuze"}]  ==> {"username": "yuze"}
        request_datas = {v.get('key'): v.get('value') for v in request_datas}
        headers = {v.get('key'): v.get('value') for v in headers}
        jsons = {v.get('key'): v.get('value') for v in jsons}
        extracts = {v.get('key'): v.get('value') for v in extracts}
        hooks = {v.get('key'): v.get('value') for v in hooks}
        # TODO: parameters 不太一样哦
        parameters = {v.get('key'): v.get('value') for v in parameters}
        validates = [cls.transact_validate(v) for v in validates]
        variables = {v.get('key'): v.get('value') for v in variables}

        # 组装请求数据
        request_data = {
            "url": form.get('url', ''),
            "headers": headers,
            "data": request_datas,
            "method": form.get("method"),
            "json": jsons
        }

        # 数据库的 request 字段内容
        req = {
            "request": request_data,
            "extract": extracts,
            "hook": hooks,
            "parameter": parameters,
            "validate": validates,
            "variable": variables,
        }

        case_info = {
            "name": form.get('name', ''),
            "type": form.get('type', 1),
            "include": str(form.get('includes', '[]')),
            "module_id": form.get('module_id'),
            "request": json.dumps(req)
        }

        return case_info

    @classmethod
    def save_by_form(cls, form):
        case_info = cls.case_info_by_form(form)
        case = cls(**case_info)
        try:
            db.session.add(case)
            db.session.commit()
            return case
        except:
            raise DatabaseException('数据库操作错误')

    def update(self, form):
        """更新测试用例"""
        case_info = self.case_info_by_form(form)

        for k, v in case_info.items():
            setattr(self, k, v)

        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            raise DatabaseException('数据库操作错误')


class SuiteInfo(Base):
    name = db.Column(db.String(128))
    includes = db.Column(db.TEXT)

    @classmethod
    def delete(cls, id):
        """并不需要删除以下的所有用例"""
        suite = cls.query.get(int(id))
        suite.status = cls.DELETE_STATUS
        try:
            db.session.add(suite)
            db.session.commit()
            return suite
        except Exception as e:
            raise e

    @classmethod
    def add_by_form(cls, form):
        suite = cls(
            name=form.name.data,
            includes=str(form.includes.data)
        )
        try:
            db.session.add(suite)
            db.session.commit()
            return suite
        except:
            raise DatabaseException('数据库操作错误')

    def update_by_form(self, form):
        """更新测试用例"""
        self.name = form.data.name
        self.includes = form.data.includes

        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            raise DatabaseException('数据库操作错误')


class User(UserMixin, Base):
    email = db.Column(db.String(64), unique=True, nullable=False)
    _pwd = db.Column("password", db.String(512))  # hash 123456

    @property
    def pwd(self):
        """获取原始密码。"""
        raise ValueError

    @pwd.setter
    def pwd(self, new_pwd):
        """设置原始密码"""
        """self.pwd=new"""
        self._pwd = generate_password_hash(new_pwd)

    def check_pwd(self, pwd_data):
        """验证密码是否正确"""
        return check_password_hash(self._pwd, pwd_data)

    @classmethod
    def insert(cls, form):
        # new = cls(email= form.email.data, _pwd=form.pwd.data)
        new = cls(email=form.email.data, pwd=form.pwd.data)
        try:
            db.session.add(new)
            db.session.commit()
            return new
        except:
            raise DatabaseException('数据库操作错误')


@login_manager.user_loader
def load_user(id):
    """"""
    return User.query.get(int(id))
