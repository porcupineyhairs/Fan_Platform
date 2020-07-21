import json

from flask import request, render_template, redirect, url_for, jsonify
from flask_login import login_required

from app.errors.exceptions import DatabaseException
from app.errors.json_errors import JsonValidateError, JsonDatabaseError
from app.main import web
from app.main.forms import SuiteAddForm, ModuleAddForm
from app.main.models import SuiteInfo, ProjectInfo


@web.route('/suites')
@login_required
def suites():
    page = request.args.get('page', 1)
    # 获取分页的 projects 信息
    paginate = SuiteInfo.paginate(page)
    suites = paginate.items
    return render_template('suites.html', suites=suites, paginate=paginate)



@web.route('/edit_suite/<int:s_id>', methods=['GET', 'POST'])
@login_required
def edit_suite(s_id=None):
    req = request.json or {}
    # 转成字符串，不然解析只能得到一个字典，而不是一个列表。
    includes = str(req['includes']) if 'includes' in req else ''
    req['includes'] = includes.replace("'", '"')
    form = SuiteAddForm(data=req)
    # 添加接口所属项目可选项
    project_choices = ProjectInfo.all()

    suite = SuiteInfo.get(s_id)
    if suite is None:
        return render_template('suites.html', form=form, projects=project_choices)
    # form.project_id.choices.extend([(str(p.id), p.project_name) for p in project_choices])
    if request.method == 'GET':
        cases = json.loads(suite.includes)
        return render_template('suite_edit.html', form=form, projects=project_choices, suite = suite, cases=cases)

    if not form.validate():
        msg = ''
        for k, v in form.errors.items():
            msg = msg.join([k, ':', v[0], '; '])
        raise JsonValidateError(msg)

    SuiteInfo.update_by_form(form)
    return jsonify({'msg': '操作成功'})


@web.route('/create_suite', methods=['GET', 'POST'])
@login_required
def create_suite():
    req = request.json or {}
    # 转成字符串，不然解析只能得到一个字典，而不是一个列表。
    includes = str(req['includes']) if 'includes' in req else  ''
    req['includes'] = includes.replace("'", '"')
    form = SuiteAddForm(data=req)
    # 添加接口所属项目可选项
    project_choices = ProjectInfo.all()
    # wtf 渲染方式：form.project_id.choices.extend([(str(p.id), p.project_name) for p in project_choices])
    if request.method == 'GET':
        return render_template('suite.html', form=form, projects=project_choices)

    if not form.validate():
        msg = ''
        for k, v in form.errors.items():
            msg = msg.join([k, ':', v[0], '; '])
        raise JsonValidateError(msg)

    SuiteInfo.add_by_form(form)
    return jsonify({'msg': '操作成功'})


@web.route('/delete_suite', methods=['POST'])
@login_required
def delete_suite():
    p_id = request.json.get('id')
    if not p_id.isdigit():
        raise JsonValidateError()
    project = SuiteInfo.get(int(p_id))
    if not project:
        raise JsonValidateError()
    # form = ModuleDeleteForm(obj=request.json)
    # if not form.validate():
    #     raise JsonValidateError()
    try:
        SuiteInfo.delete(p_id)
        return jsonify({'msg':'成功'})
    except DatabaseException:
        raise JsonDatabaseError('数据库异常')