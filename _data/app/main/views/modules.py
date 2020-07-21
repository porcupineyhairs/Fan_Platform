#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# author:muji
# datetime:2019/7/8 12:13
from flask import request, render_template, redirect, url_for, flash, abort, jsonify
from flask_login import login_required

from app.errors.exceptions import DatabaseException
from app.errors.json_errors import JsonValidateError, JsonDatabaseError
from app.main import web
from app.main.forms import ModuleAddForm
from app.main.models import ModuleInfo, ProjectInfo


@web.route('/modules')
@login_required
def list_modules():
    page = request.args.get('page', 1)
    # 获取分页的 projects 信息
    paginate = ModuleInfo.paginate(page)
    modules = paginate.items
    return render_template('modules.html', modules=modules, paginate=paginate)


@web.route('/get_module/<int:m_id>')
@login_required
def get_module(m_id=None):
    return 'get module'


@web.route('/edit_module/<int:m_id>', methods=['GET', 'POST'])
@login_required
def edit_module(m_id=None):
    module = ModuleInfo.get(m_id)
    form = ModuleAddForm(obj=module)
    # 添加可选项目
    project_choices = ProjectInfo.all()
    form.project_id.choices.extend([(str(p.id), p.project_name) for p in project_choices])

    if request.method == 'GET':
        return render_template('module_edit.html', form=form, module=module)
    if form.validate():
        module.edit_by_form(form)
        return redirect(url_for('web.list_modules'))
    return render_template('module_edit.html', form=form, module=module)


@web.route('/create_module', methods=['GET', 'POST'])
@login_required
def create_module():
    form = ModuleAddForm(request.form)
    # 添加接口所属项目可选项
    project_choices = ProjectInfo.all()
    form.project_id.choices.extend([(str(p.id), p.project_name) for p in project_choices])
    if request.method == 'GET':
        return render_template('module.html', form=form)
    if form.validate():
        ModuleInfo.add_by_form(form)
        return redirect(url_for('web.list_modules'))
    return render_template('module.html', form=form)


@web.route('/delete_module', methods=['POST'])
@login_required
def delete_module():
    p_id = request.json.get('id')
    if not p_id.isdigit():
        raise JsonValidateError()
    project = ModuleInfo.get(int(p_id))
    if not project:
        raise JsonValidateError()
    try:
        ModuleInfo.delete(p_id)
        return jsonify({'msg':'成功'})
    except DatabaseException:
        raise JsonDatabaseError('数据库异常')


