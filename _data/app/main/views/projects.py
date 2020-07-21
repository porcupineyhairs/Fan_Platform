#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# author:muji
# datetime:2019/8/1 17:20
from flask import request, render_template, redirect, url_for, jsonify
from flask_login import current_user

from app.errors.exceptions import DatabaseException
from app.errors.json_errors import JsonValidateError, JsonDatabaseError
from app.main import web
from app.main.forms import ProjectAddForm, ProjectDeleteForm
from app.main.models import ProjectInfo


@web.route('/projects')
def list_projects():
    page = request.args.get('page', 1)
    paginate = ProjectInfo.paginate(page)
    projects = paginate.items
    return render_template('projects.html', projects=projects, paginate=paginate)


@web.route('/get_project/<int:p_id>')
def get_project(p_id=None):
    return 'get project '


@web.route('/edit_project/<int:p_id>', methods=['GET', 'POST'])
def edit_project(p_id=None):
    project = ProjectInfo.get(p_id)
    if not project:
        return redirect(url_for('web.list_projects'))
    form = ProjectAddForm(obj=project)
    if request.method == 'GET':
        return render_template('project_edit.html', form=form, project=project)
    if form.validate():
        project.edit_by_form(form)
        return redirect(url_for('web.list_projects'))
    # 没有通过验证
    return render_template('project_edit.html', form=form, project=project)


@web.route('/create_project', methods=['GET', 'POST'])
def create_project():
    form = ProjectAddForm(request.form)
    if request.method == 'GET':
        return render_template('project.html', form=form)
    if form.validate():

        ProjectInfo.add_by_form(form)
        return redirect(url_for('web.list_projects'))
    print(form.errors)
    return render_template('project.html', form=form)


@web.route('/delete_project', methods=['POST'])
def delete_project():
    # 获取id
    # current_user == User()
    p_id = request.json.get('id')
    if not p_id.isdigit():
        raise JsonValidateError()
    project = ProjectInfo.get(int(p_id))
    if not project:
        raise JsonValidateError()
    try:
        ProjectInfo.delete(p_id)
        return jsonify({'msg':'成功'})
    except DatabaseException:
        raise JsonDatabaseError('数据库异常')


