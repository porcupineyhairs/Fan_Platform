#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# author:muji
# datetime:2019/8/5 14:57
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email

from app.main.forms.validators import Unique, Exist, Choose, RequestData, IncludeCaseValidate
from app.main.models import ProjectInfo, ModuleInfo, CaseInfo


class ProjectAddForm(FlaskForm):
    """添加项目表单验证"""
    # 指定对应的数据库模型
    form_model = ProjectInfo
    # 验证项
    project_name = StringField(label='项目名称', validators=[DataRequired(), Length(
        max=64, min=1), Unique(form_model, form_model.project_name)])
    simple_desc = TextAreaField(label='项目描述', validators=[Length(max=512, min=0)])


class ProjectDeleteForm(FlaskForm):
    """删除项目"""
    form_model = ProjectInfo
    id = IntegerField(label='项目ID', validators=[DataRequired(), Exist(form_model, form_model.id)])


class ModuleAddForm(FlaskForm):
    # 指定对应的数据库模型
    form_model = ModuleInfo

    module_name = StringField(label='接口名称', validators=[DataRequired(), Length(
        max=20, min=1)])
    simple_desc = TextAreaField(label='接口描述', validators=[Length(max=512, min=0)])

    project_id = SelectField(label='所属项目', choices=[(0, '全部')], validators=[
        DataRequired(), Exist(ProjectInfo, ProjectInfo.id)])
    # project_id = IntegerField(label='所属项目', validators=[
    #     DataRequired(), Exist(ProjectInfo, ProjectInfo.id)])

class ModuleDeleteForm(FlaskForm):
    form_model = ModuleInfo
    id = IntegerField(label='项目ID', validators=[DataRequired(), Exist(form_model, form_model.id)])


class CaseInfoForm(FlaskForm):
    # 指定对应的数据库模型
    form_model = CaseInfo

    # type = StringField(label='接口类型', validators=[Choose(choices=['case','module','project','suite'])])
    name = StringField(label='接口名称', validators=[DataRequired('name 不能为空'), Length(
        max=20, min=1)])
    includes = StringField(label='包含用例', validators=[Length(max=512, min=0), IncludeCaseValidate()])
    # 在视图函数中动态添加 choices 变量
    module_id = StringField(label='所属接口', validators=[Exist(ModuleInfo, ModuleInfo.id)])
    url = StringField(label='URL', default='', validators=[Length(max=512, min=1)])
    method = StringField('请求方法', validators=[Choose(choices=['GET','POST','PUT','DELETE'])])
    # 其他判断
    headers = StringField(validators=[RequestData()])
    extracts = StringField(validators=[RequestData()])
    request_datas = StringField(validators=[RequestData()])
    hooks = StringField(validators=[RequestData()])
    parameters = StringField(validators=[RequestData()])
    validates = StringField(validators=[RequestData()])
    variables = StringField(validators=[RequestData()])


class CaseIncludeForm(FlaskForm):
    project = SelectField(label='所属项目', choices=[(0, '全部')], validators=[
        DataRequired(), Exist(ProjectInfo, ProjectInfo.id)])
    module = SelectField(label='所属接口', choices=[(0, '全部')], validators=[
        DataRequired(), Exist(ModuleInfo, ModuleInfo.id)])
    case = SelectField(label='接口选择', choices=[(0, '全部')], validators=[
        DataRequired(), Exist(CaseInfo, CaseInfo.id)])


class SuiteAddForm(FlaskForm):
    name = StringField(label='套件名称', validators=[DataRequired('name 不能为空'), Length(
        max=20, min=1)])
    includes = StringField(label='包含用例', validators=[Length(max=512, min=0), IncludeCaseValidate()])

class UserRegisterEmailForm(FlaskForm):
    email = StringField(label='用户名', validators=[Length(max=64), Email()])
    pwd = StringField(label='密码', validators=[Length(max=128)])

