import json

from flask import request, render_template, jsonify
from flask_login import login_required

from app.errors.exceptions import DatabaseException
from app.main import web
from app.errors.json_errors import JsonValidateError, JsonDatabaseError
from app.main.forms import CaseInfoForm
from app.main.models import CaseInfo, ProjectInfo
from app.main.models.runner import run_single, run_batch


@web.route('/cases')
@login_required
def list_cases():
    page = request.args.get('page', 1)
    # 获取分页的 projects 信息
    paginate = CaseInfo.paginate(page)
    cases = paginate.items
    return render_template('cases.html', cases=cases, paginate=paginate)


@web.route('/get_case/<int:c_id>')
@login_required
def get_case(c_id=None):
    return 'get case '


@web.route('/edit_case/<int:c_id>', methods=['GET', 'POST'])
@login_required
def edit_case(c_id=None):
    case = CaseInfo.get(c_id)
    if not case:
        raise JsonValidateError()
    form = CaseInfoForm(obj=case)
    if request.method == 'GET':
        project_choice = ProjectInfo.all()
        return render_template('case_edit.html', form=form, project=project_choice, case=case)
    if not form.validate():
        msg = ''
        for k, v in form.errors.items():
            msg = msg.join([k, ':', v[0], '; '])
        raise JsonValidateError(msg)
    case.update(form.data)
    return jsonify({"msg": '操作成功'})


@web.route('/create_case', methods=['GET', 'POST'])
@login_required
def create_case():
    form = CaseInfoForm(data=request.json)
    project_choice = ProjectInfo.all()
    if request.method == 'GET':
        return render_template('case.html', form=form, project=project_choice)
    if not form.validate():
        # 返回 msg 信息
        msg = ''
        for k, v in form.errors.items():
            msg = msg.join([k, ':', v[0], '; '])
        raise JsonValidateError(msg)
    # 保存
    CaseInfo.save_by_form(form.data)
    return jsonify({"msg": '操作成功'})


@web.route('/delete_case', methods=['POST'])
@login_required
def delete_case():
    c_id = request.json.get('id')
    if not c_id.isdigit():
        raise JsonValidateError()
    project = CaseInfo.get(int(c_id))
    if not project:
        raise JsonValidateError()
    try:
        CaseInfo.delete(c_id)
        return jsonify({'msg': '删除成功'})
    except DatabaseException:
        raise JsonDatabaseError('数据库异常')


@web.route('/run_test', methods=['GET', 'POST'])
@login_required
def run_test():
    c_id = request.args.get('id')
    case_type = request.args.get('type')
    res = run_single(c_id, type=case_type)
    return render_template('report_template.html', **res)


@web.route('/run_test_batch', methods=['POST'])
@login_required
def run_test_batch():
    ids = request.form.get('id')
    ids = json.loads(ids)
    type = request.form.get('type')
    res = run_batch(ids, type)
    return render_template('report_template.html', **res)

# 6 个接口
# @web.route('/run_cases_by_project', methods=['POST'])
# def run_test_batch():
